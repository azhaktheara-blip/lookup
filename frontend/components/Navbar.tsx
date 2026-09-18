"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Sparkles, Sliders, Compass, LayoutDashboard, Zap, Film } from "lucide-react";

interface NavbarProps {
  credits?: number;
}

export default function Navbar({ credits = 250 }: NavbarProps) {
  const pathname = usePathname();

  const links = [
    { href: "/generator", label: "Generator", icon: Sliders },
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/explore", label: "Explore Looks", icon: Compass },
    { href: "/#pricing", label: "Pricing", icon: Zap },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/10 bg-zinc-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-zinc-950 font-black text-lg shadow-lg shadow-amber-500/20 group-hover:scale-105 transition-transform">
            TC
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold tracking-wider text-base text-zinc-100 flex items-center gap-1.5">
              THEARA COLOR
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono font-medium">
                v1.0
              </span>
            </span>
            <span className="text-[10px] tracking-widest text-zinc-400 uppercase font-medium">
              Create Your Look.
            </span>
          </div>
        </Link>

        {/* Nav Links */}
        <nav className="hidden md:flex items-center gap-1">
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-zinc-800/80 text-amber-400 border border-white/5"
                    : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900"
                }`}
              >
                <Icon className="w-4 h-4" />
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Right CTA / User / Credits */}
        <div className="flex items-center gap-3">
          {/* Credit balance badge */}
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-zinc-900 border border-white/10 text-xs font-medium text-zinc-300">
            <Zap className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
            <span className="text-amber-400 font-semibold">{credits}</span>
            <span className="text-zinc-500">credits</span>
          </div>

          <Link
            href="/generator"
            className="flex items-center gap-2 px-4 py-1.5 rounded-md bg-amber-500 hover:bg-amber-400 text-zinc-950 font-semibold text-sm transition-all shadow-md shadow-amber-500/20 hover:shadow-amber-500/30"
          >
            <Sparkles className="w-4 h-4" />
            <span>Open Studio</span>
          </Link>
        </div>
      </div>
    </header>
  );
}

