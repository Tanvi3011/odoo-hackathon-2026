"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import TopNav from "@/components/layout/TopNav";
import { useAuthStore } from "@/store/authStore";
import type { User } from "@/types";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, user, setUser, setLoading, logout } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
      logout();
      router.push("/login");
      return;
    }

    if (!user) {
      const storedUser = localStorage.getItem("user_data");
      if (storedUser) {
        setUser(JSON.parse(storedUser) as User);
      } else {
        setLoading(false);
      }
    }
  }, [logout, router, setLoading, setUser, user]);

  if (!isAuthenticated && isLoading) {
    return <div className="min-h-screen bg-background" />;
  }

  return (
    <div className="min-h-screen bg-background">
      <TopNav />
      <main className="mx-auto max-w-7xl px-6 pb-6 pt-20">{children}</main>
    </div>
  );
}
