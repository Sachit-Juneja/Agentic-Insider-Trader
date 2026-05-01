"use client";

import { useEffect, useState } from "react";
import { FinalReport } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { 
  Quote, Zap, AlertTriangle, GitMerge, Link as LinkIcon, 
  BarChart3, TrendingUp, Users, ArrowUpRight, ArrowDownRight, Database 
} from "lucide-react";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

interface DeepReportProps {
  report: FinalReport;
}

export function DeepReport({ report }: DeepReportProps) {
  const [isMounted, setIsMounted] = useState(false);
  
  useEffect(() => {
    setIsMounted(true);
  }, []);

  const sections = parseDeepReport(report.detailed_breakdown || report.final_summary);
  
  const chartData = Object.entries(report.technical_charts?.price_data || {}).map(([date, price]) => ({
    date: date.split('T')[0],
    price: Number(price)
  })).slice(-30);

  const safeNum = (val: any) => {
    const n = Number(val);
    return isNaN(n) ? 0 : n;
  };

  return (
    <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-1000 pb-20">
      
      {/* Thesis Section */}
      <section className="glass p-8 rounded-3xl relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
          <Quote size={80} className="text-[#00d4ff]" />
        </div>
        <h3 className="text-[#00d4ff] text-[10px] font-black tracking-[0.3em] uppercase mb-4 flex items-center gap-2">
          <Quote size={12} /> Executive Thesis
        </h3>
        <p className="text-2xl font-light text-slate-100 leading-tight font-serif italic mb-6">
          "{sections.thesis}"
        </p>
        
        <div className="flex gap-4">
          <Badge className="bg-[#00ff88]/10 text-[#00ff88] border-[#00ff88]/30 px-3 py-1 text-[10px] uppercase tracking-widest">
            Institutional Conviction: {report.final_score}%
          </Badge>
          <Badge className="bg-slate-800/50 text-slate-400 border-slate-700 px-3 py-1 text-[10px] uppercase tracking-widest">
            Time Horizon: {report.hold_period}
          </Badge>
        </div>
      </section>

      {/* Visual Analytics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <section className="glass p-6 rounded-3xl space-y-4 min-h-[300px]">
          <h3 className="text-slate-400 text-[10px] font-black tracking-[0.3em] uppercase flex items-center gap-2">
            <BarChart3 size={12} /> Price Trajectory (30D)
          </h3>
          <div className="h-[200px] w-full min-w-0">
            {isMounted && chartData.length > 0 && (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#00d4ff" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#00d4ff" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                  <XAxis dataKey="date" hide />
                  <YAxis hide domain={['auto', 'auto']} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', fontSize: '10px' }}
                    itemStyle={{ color: '#00d4ff' }}
                  />
                  <Area type="monotone" dataKey="price" stroke="#00d4ff" fillOpacity={1} fill="url(#colorPrice)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </section>

        <section className="glass p-6 rounded-3xl space-y-4">
          <h3 className="text-slate-400 text-[10px] font-black tracking-[0.3em] uppercase flex items-center gap-2">
            <Users size={12} /> Swarm Consensus
          </h3>
          <div className="space-y-4">
            {(report.agent_breakdown || []).slice(0, 4).map((agent, i) => (
              <div key={i} className="space-y-1">
                <div className="flex justify-between text-[10px] uppercase tracking-widest">
                  <span className="text-slate-500">{agent.name}</span>
                  <span className={agent.score >= 60 ? "text-[#00ff88]" : agent.score <= 40 ? "text-[#ff3366]" : "text-[#ffaa00]"}>
                    {agent.score}% Conviction
                  </span>
                </div>
                <div className="h-1 bg-slate-900 rounded-full overflow-hidden">
                  <div 
                    className="h-full transition-all duration-1000" 
                    style={{ 
                      width: `${agent.score}%`,
                      backgroundColor: agent.score >= 60 ? "#00ff88" : agent.score <= 40 ? "#ff3366" : "#ffaa00"
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <section className="glass p-8 rounded-3xl border-t border-t-[#00ff88]/20">
          <h3 className="text-[#00ff88] text-[10px] font-black tracking-[0.3em] uppercase mb-6 flex items-center gap-2">
            <Zap size={12} className="fill-[#00ff88]" /> Core Alpha Drivers
          </h3>
          <div className="space-y-6">
            {sections.catalysts.map((item, i) => (
              <div key={i} className="flex gap-4 items-start group">
                <div className="h-8 w-8 rounded-lg bg-[#00ff88]/10 flex items-center justify-center text-[#00ff88] text-xs font-black shrink-0">
                  {i+1}
                </div>
                <p className="text-sm text-slate-300 leading-relaxed pt-1">
                  {item}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="glass p-8 rounded-3xl border-t border-t-[#ff3366]/20">
          <h3 className="text-[#ff3366] text-[10px] font-black tracking-[0.3em] uppercase mb-6 flex items-center gap-2">
            <AlertTriangle size={12} className="fill-[#ff3366]" /> Risk Parameters
          </h3>
          <div className="space-y-6">
            {sections.risks.map((item, i) => (
              <div key={i} className="flex gap-4 items-start">
                <div className="h-8 w-8 rounded-lg bg-[#ff3366]/10 flex items-center justify-center text-[#ff3366] text-xs font-black shrink-0">
                  !
                </div>
                <p className="text-sm text-slate-300 leading-relaxed pt-1">
                  {item}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="glass p-8 rounded-3xl overflow-hidden">
        <h3 className="text-slate-400 text-[10px] font-black tracking-[0.3em] uppercase mb-6 flex items-center gap-2">
          <Database size={12} /> Smart Money Activity
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-[10px] text-slate-500 uppercase tracking-widest border-b border-slate-800">
                <th className="pb-4 font-black">Transaction Type</th>
                <th className="pb-4 font-black">Entity / Insider</th>
                <th className="pb-4 font-black">Volume / Value</th>
                <th className="pb-4 font-black">Impact</th>
              </tr>
            </thead>
            <tbody className="text-xs">
              {(report.insider_highlights?.filings || []).slice(0, 3).map((filing: any, i: number) => (
                <tr key={i} className="border-b border-slate-800/50 hover:bg-white/5 transition-colors group">
                  <td className="py-4 font-bold text-slate-300">Form 4 / {filing.transaction_type}</td>
                  <td className="py-4 text-slate-400">{filing.insider_name}</td>
                  <td className="py-4 text-slate-300">${safeNum(filing.value).toLocaleString()}</td>
                  <td className="py-4">
                    {filing.transaction_type.includes('Purchase') ? (
                      <span className="flex items-center gap-1 text-[#00ff88] uppercase font-black tracking-tighter">
                        <ArrowUpRight size={10} /> Accumulation
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-[#ff3366] uppercase font-black tracking-tighter">
                        <ArrowDownRight size={10} /> Liquidation
                      </span>
                    )}
                  </td>
                </tr>
              ))}
              {(report.flow_analysis?.unusual_trades || []).slice(0, 2).map((trade: any, i: number) => (
                <tr key={`flow-${i}`} className="border-b border-slate-800/50 hover:bg-white/5 transition-colors">
                  <td className="py-4 font-bold text-[#00d4ff]">Unusual Option / {trade.type}</td>
                  <td className="py-4 text-slate-400">{trade.contract}</td>
                  <td className="py-4 text-slate-300">${safeNum(trade.premium).toLocaleString()}</td>
                  <td className="py-4">
                    <span className="flex items-center gap-1 text-[#00d4ff] uppercase font-black tracking-tighter">
                      <TrendingUp size={10} /> High Flow
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Technical Confluence */}
      <section className="glass p-8 rounded-3xl">
        <h3 className="text-slate-400 text-[10px] font-black tracking-[0.3em] uppercase mb-4 flex items-center gap-2">
          <GitMerge size={12} /> Execution Confluence
        </h3>
        <p className="text-slate-300 text-sm leading-relaxed font-mono bg-slate-950/50 p-6 rounded-2xl border border-slate-800">
          {sections.confluence}
        </p>
      </section>

      {/* Citations */}
      <section>
        <h3 className="text-slate-500 text-[9px] font-black tracking-[0.3em] uppercase mb-4 text-center">
          Institutional Source Attribution
        </h3>
        <div className="flex flex-wrap justify-center gap-3">
          {(report.citations || []).map((cite: any, i: number) => (
            <a 
              key={i} 
              href={cite.link} 
              target="_blank" 
              className="px-4 py-2 bg-slate-900/50 border border-slate-800 rounded-xl text-[9px] text-slate-400 hover:text-[#00d4ff] hover:border-[#00d4ff] transition-all flex items-center gap-2 group"
            >
              <LinkIcon size={10} className="group-hover:rotate-45 transition-transform" />
              {cite.source} <span className="opacity-20">|</span> {cite.type}
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}

function parseDeepReport(text: string) {
  const sections = {
    thesis: "No analysis available.",
    catalysts: [] as string[],
    risks: [] as string[],
    confluence: "Data inconclusive."
  };

  if (!text) return sections;

  const thesisMatch = text.match(/THESIS:\s*([\s\S]*?)(?=\n[A-Z]+:|$)/i);
  if (thesisMatch) sections.thesis = thesisMatch[1].trim();

  const catalystsMatch = text.match(/CATALYSTS:\s*([\s\S]*?)(?=\n[A-Z]+:|$)/i);
  if (catalystsMatch) {
    sections.catalysts = catalystsMatch[1]
      .split("\n")
      .map(s => s.replace(/^[-*•\d.]+\s*/, "").trim())
      .filter(s => s.length > 5);
  }

  const risksMatch = text.match(/RISKS:\s*([\s\S]*?)(?=\n[A-Z]+:|$)/i);
  if (risksMatch) {
    sections.risks = risksMatch[1]
      .split("\n")
      .map(s => s.replace(/^[-*•\d.]+\s*/, "").trim())
      .filter(s => s.length > 5);
  }

  const confluenceMatch = text.match(/CONFLUENCE:\s*([\s\S]*?)(?=\n[A-Z]+:|$)/i);
  if (confluenceMatch) sections.confluence = confluenceMatch[1].trim();

  return sections;
}
