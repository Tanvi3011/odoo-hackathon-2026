"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { LeaveRequest } from "@/types";

export default function LeavesPage() {
  const { user } = useAuthStore();
  const isAdmin = user?.role === "admin" || user?.role === "hr";
  const [leaves, setLeaves] = useState<LeaveRequest[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchLeaves = async () => {
    setLoading(true);
    try {
      const endpoint = isAdmin ? "/leaves/" : "/leaves/my";
      const res = await api.get(endpoint);
      setLeaves(res.data.data);
    } catch (err) {
      console.error("Failed to fetch leaves", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeaves();
  }, [isAdmin]);

  const handleAction = async (id: string, status: "approved" | "rejected") => {
    try {
      await api.put(`/leaves/${id}`, { status });
      fetchLeaves();
    } catch (err) {
      console.error("Failed to process leave", err);
    }
  };

  const getStatusClass = (status: string) => {
    switch (status) {
      case "approved":
        return "bg-success/10 text-success border-success/20";
      case "rejected":
        return "bg-danger/10 text-danger border-danger/20";
      case "pending":
        return "bg-warning/10 text-warning border-warning/20";
      default:
        return "bg-muted text-text-secondary";
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-foreground">Time Off</h1>
        {!isAdmin && <Button className="bg-secondary text-white hover:bg-secondary-hover">Apply for Leave</Button>}
      </div>

      <div className="overflow-hidden rounded-lg border border-border bg-card shadow-sm">
        <Table>
          <TableHeader>
            <TableRow className="border-border bg-muted/50">
              {isAdmin && <TableHead className="text-text-secondary">Employee</TableHead>}
              <TableHead className="text-text-secondary">Type</TableHead>
              <TableHead className="text-text-secondary">Dates</TableHead>
              <TableHead className="text-text-secondary">Days</TableHead>
              <TableHead className="text-text-secondary">Status</TableHead>
              {isAdmin && <TableHead className="text-right text-text-secondary">Actions</TableHead>}
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              Array.from({ length: 3 }).map((_, index) => (
                <TableRow key={index}>
                  {isAdmin && <TableCell><Skeleton className="h-4 w-24" /></TableCell>}
                  <TableCell><Skeleton className="h-4 w-20" /></TableCell>
                  <TableCell><Skeleton className="h-4 w-32" /></TableCell>
                  <TableCell><Skeleton className="h-4 w-8" /></TableCell>
                  <TableCell><Skeleton className="h-4 w-16" /></TableCell>
                  {isAdmin && <TableCell><Skeleton className="ml-auto h-4 w-24" /></TableCell>}
                </TableRow>
              ))
            ) : leaves.length === 0 ? (
              <TableRow>
                <TableCell colSpan={isAdmin ? 6 : 5} className="py-8 text-center text-text-secondary">
                  No leave requests found.
                </TableCell>
              </TableRow>
            ) : (
              leaves.map((leave) => (
                <TableRow key={leave.id} className="border-border">
                  {isAdmin && <TableCell className="font-medium text-foreground">{leave.employee_name}</TableCell>}
                  <TableCell className="text-text-secondary">{leave.leave_type.replace("_", " ")}</TableCell>
                  <TableCell className="text-text-secondary">
                    {new Date(leave.start_date).toLocaleDateString()} - {new Date(leave.end_date).toLocaleDateString()}
                  </TableCell>
                  <TableCell className="text-text-secondary">{leave.days}</TableCell>
                  <TableCell>
                    <span className={`rounded-full border px-2 py-1 text-xs ${getStatusClass(leave.status)}`}>
                      {leave.status}
                    </span>
                  </TableCell>
                  {isAdmin && leave.status === "pending" && (
                    <TableCell className="space-x-2 text-right">
                      <Button size="sm" variant="outline" className="border-success text-success hover:bg-success hover:text-white" onClick={() => handleAction(leave.id, "approved")}>
                        Approve
                      </Button>
                      <Button size="sm" variant="outline" className="border-danger text-danger hover:bg-danger hover:text-white" onClick={() => handleAction(leave.id, "rejected")}>
                        Reject
                      </Button>
                    </TableCell>
                  )}
                  {isAdmin && leave.status !== "pending" && <TableCell />}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
