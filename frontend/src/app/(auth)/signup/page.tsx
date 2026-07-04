"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { UserCircle } from "lucide-react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const schema = z
  .object({
    company_name: z.string().min(2, "Company name is required"),
    first_name: z.string().min(1, "First name is required"),
    last_name: z.string().min(1, "Last name is required"),
    email: z.string().email("Invalid email"),
    phone: z.string().optional(),
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirm_password: z.string(),
    role: z.enum(["employee", "hr"]),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
  });

type SignupFormValues = z.infer<typeof schema>;

export default function SignupPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignupFormValues>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: SignupFormValues) => {
    try {
      await api.post("/auth/register", data);
      router.push("/login");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-lg bg-card border border-border rounded-lg shadow-sm p-8">
        <div className="flex flex-col items-center mb-6">
          <UserCircle className="w-12 h-12 text-secondary mb-4" />
          <h1 className="text-2xl font-bold text-foreground">Create Account</h1>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Label htmlFor="company_name">Company Name</Label>
            <Input id="company_name" placeholder="Acme Inc." {...register("company_name")} />
            {errors.company_name && <p className="text-danger text-sm mt-1">{errors.company_name.message}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="first_name">First Name</Label>
              <Input id="first_name" placeholder="John" {...register("first_name")} />
              {errors.first_name && <p className="text-danger text-sm mt-1">{errors.first_name.message}</p>}
            </div>
            <div>
              <Label htmlFor="last_name">Last Name</Label>
              <Input id="last_name" placeholder="Doe" {...register("last_name")} />
              {errors.last_name && <p className="text-danger text-sm mt-1">{errors.last_name.message}</p>}
            </div>
          </div>

          <div>
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="john@acme.com" {...register("email")} />
            {errors.email && <p className="text-danger text-sm mt-1">{errors.email.message}</p>}
          </div>

          <div>
            <Label htmlFor="role">Role</Label>
            <select
              id="role"
              className="flex h-10 w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-foreground shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-secondary focus-visible:ring-offset-2"
              {...register("role")}
              defaultValue="employee"
            >
              <option value="employee">Employee</option>
              <option value="hr">HR</option>
            </select>
            {errors.role && <p className="text-danger text-sm mt-1">{errors.role.message}</p>}
          </div>

          <div>
            <Label htmlFor="phone">Phone (Optional)</Label>
            <Input id="phone" placeholder="+1 234 567 890" {...register("phone")} />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" placeholder="********" {...register("password")} />
              {errors.password && <p className="text-danger text-sm mt-1">{errors.password.message}</p>}
            </div>
            <div>
              <Label htmlFor="confirm_password">Confirm Password</Label>
              <Input id="confirm_password" type="password" placeholder="********" {...register("confirm_password")} />
              {errors.confirm_password && <p className="text-danger text-sm mt-1">{errors.confirm_password.message}</p>}
            </div>
          </div>

          {error && <p className="text-danger text-sm text-center">{error}</p>}

          <Button type="submit" disabled={isSubmitting} className="w-full bg-primary hover:bg-primary-hover text-white h-11">
            {isSubmitting ? "Creating Account..." : "Create Account"}
          </Button>
        </form>

        <p className="text-text-secondary text-sm text-center mt-6">
          Already have an account?{" "}
          <Link href="/login" className="text-secondary hover:underline">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}
