"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

interface AttendanceRecord {
  employee_id: string;
  employee_name: string;
  date: string;
  check_in?: string;
  check_out?: string;
  work_hours: number;
  status: string;
}

export default function AttendancePage() {
  const { user } = useAuthStore();
  const isAdmin = user?.role === "admin" || user?.role === "hr";
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCheckedIn, setIsCheckedIn] = useState(false);

  const today = new Date().toISOString().split("T")[0];

  useEffect(() => {
    const fetchAttendance = async () => {
      try {
        const endpoint = isAdmin ? `/attendance/?start_date=${today}&end_date=${today}` : `/attendance/me?start_date=${today}&end_date=${today}`;
        const res = await api.get(endpoint);
        setRecords(res.data.data);

        if (!isAdmin && res.data.data.length > 0 && res.data.data[0].check_in && !res.data.data[0].check_out) {
          setIsCheckedIn(true);
        }
      } catch (err) {
        console.error("Failed to fetch attendance", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAttendance();
  }, [isAdmin, today]);

  const handleCheckInOut = async () => {
    try {
      const endpoint = isCheckedIn ? "/attendance/check-out" : "/attendance/check-in";
      await api.post(endpoint);

      const res = await api.get(`/attendance/me?start_date=${today}&end_date=${today}`);
      setRecords(res.data.data);
      setIsCheckedIn(!isCheckedIn);
    } catch (err) {
      console.error("Check-in/out failed", err);
    }
  };

  const getStatusClass = (status: string) => {
    switch (status) {
      case "present":
        return "bg-success/10 text-success border-success/20";
      case "absent":
        return "bg-danger/10 text-danger border-danger/20";
      case "half_day":
        return "bg-warning/10 text-warning border-warning/20";
      case "leave":
        return "bg-info/10 text-info border-info/20";
      default:
        return "bg-muted text-text-secondary";
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-foreground">Attendance</h1>
        {!isAdmin && (
          <Button onClick={handleCheckInOut} className={isCheckedIn ? "bg-primary hover:bg-primary-hover" : "bg-secondary hover:bg-secondary-hover"}>
            {isCheckedIn ? "Check Out" : "Check In"}
          </Button>
        )}
      </div>

      <div className="overflow-hidden rounded-lg border border-border bg-card shadow-sm">
        <Table>
          <TableHeader>
            <TableRow className="border-border bg-muted/50">
              {isAdmin && <TableHead className="text-text-secondary">Employee</TableHead>}
              <TableHead className="text-text-secondary">Date</TableHead>
              <TableHead className="text-text-secondary">Check In</TableHead>
              <TableHead className="text-text-secondary">Check Out</TableHead>
              <TableHead className="text-text-secondary">Hours</TableHead>
              <TableHead className="text-text-secondary">Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              Array.from({ length: 3 }).map((_, index) => (
                <TableRow key={index}>
                  <TableCell><Skeleton className="h-4 w-24" /></TableCell>
                  <TableCell><Skeleton className="h-4 w-20" /></TableCell>
                  <TableCell><Skeleton className="h-4 w-16" /></TableCell>
                  <TableCell><Skeleton className="h-4 w-16" /></TableCell>
                  <TableCell><Skeleton className="h-4 w-10" /></TableCell>
                  <TableCell><Skeleton className="h-4 w-16" /></TableCell>
                </TableRow>
              ))
            ) : records.length === 0 ? (
              <TableRow>
                <TableCell colSpan={isAdmin ? 6 : 5} className="py-8 text-center text-text-secondary">
                  No attendance records for today.
                </TableCell>
              </TableRow>
            ) : (
              records.map((record, index) => (
                <TableRow key={index} className="border-border">
                  {isAdmin && <TableCell className="font-medium text-foreground">{record.employee_name}</TableCell>}
                  <TableCell className="text-text-secondary">{record.date}</TableCell>
                  <TableCell className="text-text-secondary">{record.check_in ? new Date(record.check_in).toLocaleTimeString() : "-"}</TableCell>
                  <TableCell className="text-text-secondary">{record.check_out ? new Date(record.check_out).toLocaleTimeString() : "-"}</TableCell>
                  <TableCell className="text-text-secondary">{record.work_hours || 0}h</TableCell>
                  <TableCell>
                    <span className={`rounded-full border px-2 py-1 text-xs ${getStatusClass(record.status)}`}>
                      {record.status.replace("_", " ")}
                    </span>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
