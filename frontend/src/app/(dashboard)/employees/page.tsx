"use client";

import { useEffect, useState } from "react";
import { Search } from "lucide-react";
import api from "@/lib/api";
import { Input } from "@/components/ui/input";
import EmployeeCard from "@/components/dashboard/EmployeeCard";
import { Skeleton } from "@/components/ui/skeleton";
import type { EmployeeCardData } from "@/types";

export default function EmployeesPage() {
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

    fetchEmployees();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-foreground">Directory</h1>

      <div className="flex flex-col gap-4 sm:flex-row">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" />
          <Input placeholder="Search by name or ID..." className="border-border bg-card pl-10" />
        </div>
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
        ) : employees.length === 0 ? (
          <p className="text-text-secondary">No employees found.</p>
        ) : (
          employees.map((emp) => <EmployeeCard key={emp.employee_id} employee={emp} />)
        )}
      </div>
    </div>
  );
}
