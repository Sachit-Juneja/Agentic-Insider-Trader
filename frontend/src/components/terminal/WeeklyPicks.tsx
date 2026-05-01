"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, ArrowUpRight, ShieldCheck, Zap, BarChart3, Info } from "lucide-react";
import { motion } from "framer-motion";

interface Pick {
  ticker: string;
  rating: string;
  score: number;
  predicted_increase: string;
  reason: string;
  confidence: number;
  catalysts: string[];
}

export function WeeklyPicks() {
  const [picks, setPicks] = useState<Pick[]>([]);
  const [loading, setLoading] = useState(true);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    fetch("http://localhost:8000/api/weekly-picks")
      .then((res) => res.json())
      .then((data) => {
        setPicks(data.picks);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (!isMounted) return null;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[400px] text-slate-500 animate-pulse uppercase tracking-[0.3em] text-[10px] font-black">
        Scanning Global Markets for Alpha...
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {picks.map((pick, i) => (
        <motion.div 
          key={pick.ticker} 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          className="glass p-8 rounded-3xl group relative overflow-hidden flex flex-col h-full"
        >
          {/* Subtle background glow */}
          <div className="absolute top-0 right-0 w-32 h-32 bg-[#00d4ff]/5 blur-[60px] group-hover:bg-[#00d4ff]/10 transition-all" />
          
          <div className="flex justify-between items-start mb-6">
            <div className="space-y-1">
              <h3 className="text-4xl font-black tracking-tighter text-white group-hover:text-[#00d4ff] transition-colors flex items-baseline gap-2">
                {pick.ticker}
                <span className="text-xs font-black text-[#00ff88] tracking-[0.2em] uppercase">
                  {pick.predicted_increase}
                </span>
              </h3>
              <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                <ShieldCheck size={10} className="text-emerald-500" /> Confidence: {(pick.confidence * 100).toFixed(0)}%
              </div>
            </div>
            <div className="text-right">
              <Badge className={`px-3 py-1 text-[10px] font-black uppercase tracking-widest ${
                pick.rating.includes("STRONG") ? "bg-[#00ff88]/20 text-[#00ff88] border-[#00ff88]/30" : "bg-[#00d4ff]/20 text-[#00d4ff] border-[#00d4ff]/30"
              }`}>
                {pick.rating}
              </Badge>
              <div className="text-[9px] font-bold text-slate-600 mt-2">Score: {pick.score}/100</div>
            </div>
          </div>

          <p className="text-sm text-slate-300 leading-relaxed font-medium mb-8 grow">
            {pick.reason}
          </p>

          <div className="space-y-4">
            <h4 className="text-[9px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
              <Zap size={10} className="text-amber-500 fill-amber-500" /> Key Catalysts
            </h4>
            <div className="flex flex-wrap gap-2">
              {pick.catalysts.map((cat, j) => (
                <span key={j} className="px-3 py-1 bg-slate-900/50 border border-slate-800 rounded-lg text-[9px] font-bold text-slate-400">
                  {cat}
                </span>
              ))}
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-slate-800/50 flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="flex flex-col">
                <span className="text-[8px] font-black text-slate-600 uppercase">Flow Bias</span>
                <span className="text-[10px] font-black text-[#00d4ff] uppercase">Institutional</span>
              </div>
              <div className="h-4 w-[1px] bg-slate-800" />
              <div className="flex flex-col">
                <span className="text-[8px] font-black text-slate-600 uppercase">Regime</span>
                <span className="text-[10px] font-black text-emerald-400 uppercase">Risk-On</span>
              </div>
            </div>
            <button className="h-8 w-8 rounded-full bg-slate-900 flex items-center justify-center text-slate-500 hover:text-[#00d4ff] hover:bg-[#00d4ff]/10 transition-all">
              <ArrowUpRight size={14} />
            </button>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
