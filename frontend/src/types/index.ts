export interface User {
  employee_id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  address?: string;
  department?: string;
  designation?: string;
  date_of_joining: string;
  profile_picture?: string;
  company_name: string;
  role: "employee" | "admin" | "hr";
  first_login?: boolean;
  salary?: SalaryStructure;
}

export interface SalaryStructure {
  monthly_wage: number;
  yearly_wage: number;
  basic_salary: number;
  hra: number;
  allowances: number;
  pf_contribution: number;
  professional_tax: number;
  other_deductions: number;
  performance_bonus: number;
  gross_salary: number;
  total_deductions: number;
  net_salary: number;
}

export interface EmployeeCardData {
  employee_id: string;
  first_name: string;
  last_name: string;
  department?: string;
  designation?: string;
  profile_picture?: string;
  status: "present" | "absent" | "half_day" | "leave";
}

export interface LeaveRequest {
  id: string;
  employee_name: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  days: number;
  status: "pending" | "approved" | "rejected";
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
  timestamp: string;
}
