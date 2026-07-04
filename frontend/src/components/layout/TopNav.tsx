"use client";

import { usePathname, useRouter } from "next/navigation";
import { Building2, LogOut, User as UserIcon } from "lucide-react";
import { useAuthStore } from "@/store/authStore";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";

export default function TopNav() {
  const { user, logout } = useAuthStore();
  const router = useRouter();
  const pathname = usePathname();

  const isAdmin = user?.role === "admin" || user?.role === "hr";

  const navItems = [
    { label: "Employees", href: "/employees", adminOnly: true },
    { label: "Attendance", href: "/attendance", adminOnly: false },
    { label: "Time-Off", href: "/leaves", adminOnly: false },
  ].filter((item) => !item.adminOnly || isAdmin);

  return (
    <nav className="fixed left-0 right-0 top-0 z-50 flex h-16 items-center justify-between border-b border-border bg-card px-6">
      <div className="flex items-center gap-2">
        <Building2 className="h-6 w-6 text-secondary" />
        <span className="font-semibold text-foreground">HRMS</span>
      </div>

      <div className="flex items-center gap-6">
        {navItems.map((item) => (
          <button
            key={item.href}
            onClick={() => router.push(item.href)}
            className={`text-sm font-medium transition-colors ${
              pathname.startsWith(item.href) ? "border-b-2 border-secondary text-secondary" : "text-text-secondary hover:text-foreground"
            }`}
          >
            {item.label}
          </button>
        ))}
      </div>

      <DropdownMenu>
        <DropdownMenuTrigger>
          <Avatar className="h-10 w-10 cursor-pointer">
            <AvatarImage src={user?.profile_picture} />
            <AvatarFallback className="bg-muted text-foreground">
              {user?.first_name?.[0]}
              {user?.last_name?.[0]}
            </AvatarFallback>
          </Avatar>
        </DropdownMenuTrigger>

        <DropdownMenuContent align="end" className="border-border bg-card">
          <DropdownMenuItem onClick={() => router.push(`/profile/${user?.employee_id}`)}>
            <UserIcon className="mr-2 h-4 w-4" /> My Profile
          </DropdownMenuItem>
          <DropdownMenuItem
            onClick={() => {
              logout();
              router.push("/login");
            }}
          >
            <LogOut className="mr-2 h-4 w-4" /> Log Out
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </nav>
  );
}
