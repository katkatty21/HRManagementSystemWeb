from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
from .models import (
    EmployeeSalary, 
    PayrollPeriod, 
    PayrollRecord,
    PayrollCorrectionRequest,
    PayrollAdjustment,
    EmployeeInformation
)
from hraccount.models import UserAccount
from .forms import (
    PayrollPeriodForm,
    PayrollCorrectionRequestForm,
    PayrollAdjustmentForm
)
import csv
from django.utils import timezone

def is_admin(user):
    return user.role == 'Admin'

# Admin Views
@login_required
@user_passes_test(is_admin)
def manage_payroll_period(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        period_type = request.POST.get('period_type')
        
        PayrollPeriod.objects.create(
            start_date=start_date,
            end_date=end_date,
            period_type=period_type
        )
        messages.success(request, 'Payroll period created successfully.')
        return redirect('payroll_periods')
    
    periods = PayrollPeriod.objects.all().order_by('-start_date')
    return render(request, 'hrmanagement/admin/payroll_periods.html', {'periods': periods})

@login_required
@user_passes_test(is_admin)
def manage_employee_salary(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        pay_type = request.POST.get('pay_type')
        base_salary = request.POST.get('base_salary')
        effective_date = request.POST.get('effective_date')
        
        try:
            employee = EmployeeInformation.objects.get(employee_id__account_id=employee_id)
            
            EmployeeSalary.objects.update_or_create(
                employee=employee,
                defaults={
                    'pay_type': pay_type,
                    'base_salary': base_salary,
                    'effective_date': effective_date
                }
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Employee salary updated successfully'
                })
            
            messages.success(request, 'Employee salary updated successfully')
            return redirect('employee_salaries')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=400)
            
            messages.error(request, f'Error: {str(e)}')
            return redirect('employee_salaries')
    
    # Get all employees (excluding admins)
    employees = EmployeeInformation.objects.select_related('employee_id').filter(
        employee_id__role='User'
    ).exclude(employee_id__role='Admin')
    
    # Get all salaries
    salaries = EmployeeSalary.objects.select_related('employee').all()
    
    return render(request, 'hrmanagement/admin/employee_salaries.html', {
        'employees': employees,
        'salaries': salaries
    })

@login_required
@user_passes_test(is_admin)
def manage_payroll_adjustment(request):
    adjustments = PayrollAdjustment.objects.all().order_by('-date_added')
    form = PayrollAdjustmentForm()
    
    if request.method == 'POST':
        adjustment_id = request.GET.get('id')
        action = request.POST.get('action')
        
        if action == 'delete' and adjustment_id:
            adjustment = get_object_or_404(PayrollAdjustment, id=adjustment_id)
            adjustment.delete()
            messages.success(request, 'Payroll adjustment deleted successfully.')
            return redirect('hrmanagement:payroll_adjustments')
            
        if adjustment_id:
            adjustment = get_object_or_404(PayrollAdjustment, id=adjustment_id)
            form = PayrollAdjustmentForm(request.POST, instance=adjustment)
        else:
            form = PayrollAdjustmentForm(request.POST)
            
        if form.is_valid():
            form.save()
            messages.success(request, 'Payroll adjustment saved successfully.')
            return redirect('hrmanagement:payroll_adjustments')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    context = {
        'adjustments': adjustments,
        'form': form
    }
    return render(request, 'hrmanagement/admin/payroll_adjustments.html', context)

@login_required
@user_passes_test(is_admin)
def process_payroll(request, period_id):
    period = get_object_or_404(PayrollPeriod, uuid=period_id)
    
    if request.method == 'POST':
        if not period.is_processed:
            employees = EmployeeInformation.objects.filter(is_active=True)
            
            for employee in employees:
                try:
                    salary = EmployeeSalary.objects.get(employee=employee)
                    
                    # Calculate bonuses and deductions
                    bonuses = PayrollAdjustment.objects.filter(
                        employee=employee,
                        payroll_period=period,
                        adjustment_type='BONUS'
                    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
                    
                    deductions = PayrollAdjustment.objects.filter(
                        employee=employee,
                        payroll_period=period,
                        adjustment_type='DEDUCTION'
                    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
                    
                    # Calculate net salary
                    net_salary = salary.base_salary + bonuses - deductions
                    
                    # Create payroll record
                    PayrollRecord.objects.create(
                        employee=employee,
                        payroll_period=period,
                        base_salary=salary.base_salary,
                        total_bonus=bonuses,
                        total_deduction=deductions,
                        net_salary=net_salary,
                        is_finalized=True
                    )
                except EmployeeSalary.DoesNotExist:
                    messages.warning(request, f'No salary information found for {employee.get_full_name()}')
                    continue
            
            period.is_processed = True
            period.save()
            messages.success(request, 'Payroll processed successfully.')
            return redirect('payroll_periods')
    
    context = {
        'period': period,
    }
    return render(request, 'hrmanagement/admin/process_payroll.html', context)

@login_required
@user_passes_test(is_admin)
def export_payroll(request, period_id):
    period = get_object_or_404(PayrollPeriod, uuid=period_id)
    records = PayrollRecord.objects.filter(payroll_period=period)
    
    export_format = request.GET.get('format', 'pdf')
    
    if export_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="payroll_{period.start_date}_{period.end_date}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Employee', 'Base Salary', 'Total Bonus', 'Total Deduction', 'Net Salary'])
        
        for record in records:
            writer.writerow([
                f"{record.employee.first_name} {record.employee.last_name}",
                record.base_salary,
                record.total_bonus,
                record.total_deduction,
                record.net_salary
            ])
        
        return response
    else:  # PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="payroll_{period.start_date}_{period.end_date}.pdf"'
        
        # Create the PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            alignment=1,  # Center alignment
            spaceAfter=30
        )
        
        # Add title
        elements.append(Paragraph('Payroll Report', title_style))
        elements.append(Paragraph(f'Period: {period.period_type}', styles['Normal']))
        elements.append(Paragraph(f'Date Range: {period.start_date} to {period.end_date}', styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Create table data
        data = [['Employee', 'Base Salary', 'Total Bonus', 'Total Deduction', 'Net Salary']]
        for record in records:
            data.append([
                f"{record.employee.first_name} {record.employee.last_name}",
                str(record.base_salary),
                str(record.total_bonus),
                str(record.total_deduction),
                str(record.net_salary)
            ])
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        return response

@login_required
@user_passes_test(is_admin)
def manage_correction_requests(request):
    correction_requests = PayrollCorrectionRequest.objects.select_related(
        'employee', 'payroll_record'
    ).order_by('-date_submitted')
    return render(request, 'hrmanagement/admin/correction_requests.html', {
        'correction_requests': correction_requests
    })

@login_required
@user_passes_test(is_admin)
def approve_correction_request(request, request_id):
    correction_request = get_object_or_404(PayrollCorrectionRequest, id=request_id)
    correction_request.status = 'APPROVED'
    correction_request.processed_at = timezone.now()
    correction_request.processed_by = request.user
    correction_request.save()
    messages.success(request, 'Correction request approved successfully.')
    return redirect('correction_requests')

@login_required
@user_passes_test(is_admin)
def reject_correction_request(request, request_id):
    correction_request = get_object_or_404(PayrollCorrectionRequest, id=request_id)
    correction_request.status = 'REJECTED'
    correction_request.processed_at = timezone.now()
    correction_request.processed_by = request.user
    correction_request.save()
    messages.success(request, 'Correction request rejected successfully.')
    return redirect('correction_requests')

# Employee Views
@login_required
def view_payroll(request):
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user)
        records = PayrollRecord.objects.filter(employee=employee).order_by('-payroll_period__start_date')
        return render(request, 'hrmanagement/employee/view_payroll.html', {
            'records': records
        })
    except EmployeeInformation.DoesNotExist:
        messages.error(request, 'Employee information not found.')
        return redirect('user_home')

@login_required
def view_payroll_detail(request, record_id):
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user)
        record = get_object_or_404(PayrollRecord, id=record_id, employee=employee)
        return render(request, 'hrmanagement/employee/view_payroll_detail.html', {
            'record': record
        })
    except EmployeeInformation.DoesNotExist:
        messages.error(request, 'Employee information not found.')
        return redirect('hraccount:user_home')

@login_required
def submit_correction_request(request):
    if request.method == 'POST':
        try:
            employee = EmployeeInformation.objects.get(employee_id=request.user)
            record_id = request.POST.get('record_id')
            description = request.POST.get('description')
            
            record = get_object_or_404(PayrollRecord, id=record_id, employee=employee)
            
            PayrollCorrectionRequest.objects.create(
                employee=employee,
                payroll_record=record,
                description=description
            )
            
            messages.success(request, 'Correction request submitted successfully.')
            return redirect('view_payroll')
            
        except Exception as e:
            messages.error(request, f'Error submitting correction request: {str(e)}')
            return redirect('view_payroll')
    
    return redirect('view_payroll')

@login_required
def download_payslip(request, record_id):
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user)
        record = get_object_or_404(PayrollRecord, id=record_id, employee=employee)
        
        # Create the HttpResponse object with PDF headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="payslip_{record.payroll_period.start_date.strftime("%Y%m")}.pdf"'
        
        # Create the PDF object using reportlab
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        # Add title
        elements.append(Paragraph("PAYSLIP", title_style))
        elements.append(Spacer(1, 12))
        
        # Add employee information
        data = [
            ['Employee Information', ''],
            ['Name:', f"{record.employee.first_name} {record.employee.last_name}"],
            ['Department:', str(record.employee.job.department.department_name)],
            ['Position:', str(record.employee.job.job_title)],
            ['Pay Period:', f"{record.payroll_period.start_date.strftime('%B %d, %Y')} - {record.payroll_period.end_date.strftime('%B %d, %Y')}"],
            ['', ''],
            ['Earnings', ''],
            ['Base Salary:', f"P{record.base_salary:,.2f}"],
            ['Total Bonus:', f"P{record.total_bonus:,.2f}"],
            ['Total Deduction:', f"P{record.total_deduction:,.2f}"],
            ['Net Pay:', f"P{record.net_salary:,.2f}"],
        ]
        
        # Create table
        table = Table(data, colWidths=[4*inch, 3*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.grey),
            ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),  # Earnings header
            ('TEXTCOLOR', (0, 6), (-1, 6), colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),  # Line above total
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Make total bold
        ]))
        elements.append(table)
        
        # Add adjustments details
        adjustments = PayrollAdjustment.objects.filter(
            employee=record.employee,
            payroll_period=record.payroll_period
        )
        if adjustments:
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Adjustments", styles['Heading2']))
            data = []
            for adj in adjustments:
                data.append([adj.get_adjustment_type_display(), adj.description, f"P{adj.amount:,.2f}"])
            table = Table(data, colWidths=[2*inch, 3*inch, 2*inch])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.grey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer and write it to the response
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
        
    except EmployeeInformation.DoesNotExist:
        messages.error(request, 'Employee information not found.')
        return redirect('hraccount:user_home')
