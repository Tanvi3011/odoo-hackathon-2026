"use client";

import { useEffect, useState } from "react";
import { Search } from "lucide-react";
import { useAuthStore } from "@/store/authStore";
import api from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import EmployeeCard from "@/components/dashboard/EmployeeCard";
import { Skeleton } from "@/components/ui/skeleton";
import type { EmployeeCardData } from "@/types";

export default function DashboardPage() {
  const { user } = useAuthStore();
  const isAdmin = user?.role === "admin" || user?.role === "hr";
  const [employees, setEmployees] = useState<EmployeeCardData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const res = await api.get("/employees/");
        setEmployees(res.data.data);
      } catch (err) {
        console.error("Failed to fetch employees", err);
      } finally {
        setLoading(false);
      }
    };

    if (isAdmin) fetchEmployees();
    else setLoading(false);
  }, [isAdmin]);

  if (!isAdmin) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-foreground">Welcome back, {user?.first_name || "Employee"} 👋</h1>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          <div className="cursor-pointer rounded-lg border border-border bg-card p-6 shadow-sm transition-all hover:border-secondary">
            <h3 className="mb-2 font-semibold text-foreground">Attendance</h3>
            <p className="text-sm text-text-secondary">Check in or check out for today.</p>
          </div>

          <div className="cursor-pointer rounded-lg border border-border bg-card p-6 shadow-sm transition-all hover:border-secondary">
            <h3 className="mb-2 font-semibold text-foreground">My Leaves</h3>
            <p className="text-sm text-text-secondary">Apply for time off or view status.</p>
          </div>

          <div className="cursor-pointer rounded-lg border border-border bg-card p-6 shadow-sm transition-all hover:border-secondary">
            <h3 className="mb-2 font-semibold text-foreground">My Payroll</h3>
            <p className="text-sm text-text-secondary">View your salary structure.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-foreground">Employees</h1>
      </div>

      <div className="flex flex-col gap-4 sm:flex-row">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" />
          <Input placeholder="Search by name or ID..." className="border-border bg-card pl-10" />
        </div>
        <Button variant="outline" className="border-border text-text-secondary hover:bg-muted">
          Filter by Department
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {loading ? (
          Array.from({ length: 8 }).map((_, index) => (
            <div key={index} className="flex h-64 flex-col items-center justify-center rounded-lg border border-border bg-card p-6">
              <Skeleton className="mb-4 h-20 w-20 rounded-full" />
              <Skeleton className="mb-2 h-4 w-32" />
              <Skeleton className="h-3 w-24" />
            </div>
          ))
        ) : (
          employees.map((emp) => <EmployeeCard key={emp.employee_id} employee={emp} />)
        )}
      </div>
    </div>
  );
}