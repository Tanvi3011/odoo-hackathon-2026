import * as React from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import type { EmployeeCardData } from "@/types";

interface EmployeeCardProps {
  employee: EmployeeCardData;
}

const statusColors: Record<EmployeeCardData["status"], string> = {
  present: "bg-success",
  absent: "bg-danger",
  half_day: "bg-warning",
  leave: "bg-info",
};

export default function EmployeeCard({ employee }: EmployeeCardProps) {
  const initials = `${employee.first_name[0]}${employee.last_name[0]}`;
  const fallbackSeed = `${employee.first_name}+${employee.last_name}`;
  const avatarSrc = employee.profile_picture || `https://api.dicebear.com/7.x/initials/svg?seed=${fallbackSeed}`;

  return React.createElement(
    "div",
    {
      className:
        "flex h-64 cursor-pointer flex-col items-center justify-center rounded-lg border border-border bg-card p-6 transition-all hover:border-secondary hover:shadow-md",
    },
    React.createElement(
      "div",
      { className: "relative mb-4" },
      React.createElement(
        Avatar,
        { className: "h-20 w-20 border-2 border-muted" },
        React.createElement(AvatarImage, { src: avatarSrc }),
        React.createElement(AvatarFallback, { className: "bg-primary text-xl font-semibold text-white" }, initials)
      ),
      React.createElement("span", {
        className: `absolute bottom-1 right-1 h-4 w-4 rounded-full border-2 border-card ${statusColors[employee.status]}`,
      })
    ),
    React.createElement(
      "h3",
      { className: "text-center text-lg font-semibold text-foreground" },
      employee.first_name,
      " ",
      employee.last_name
    ),
    React.createElement("p", { className: "mb-2 text-center text-sm text-text-muted" }, employee.employee_id),
    employee.designation
      ? React.createElement(
          "p",
          { className: "text-center text-sm text-text-secondary" },
          employee.designation,
          ", ",
          employee.department
        )
      : employee.department
        ? React.createElement(
            "span",
            { className: "mt-2 rounded-md bg-muted px-2 py-1 text-xs text-text-secondary" },
            employee.department
          )
        : null
  );
}