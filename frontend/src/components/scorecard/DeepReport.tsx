"use client";

import { FinalReport } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Quote, Zap, AlertTriangle, GitMerge, Link as LinkIcon } from "lucide-react";

interface DeepReportProps {
  report: FinalReport;
}

export function DeepReport({ report }: DeepReportProps) {
  // Parse the structured report from the LLM
  const sections = parseDeepReport(report.detailed_breakdown || report.final_summary);

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
      
      {/* Thesis Section */}
      <section className="glass p-8 rounded-2xl relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
          <Quote size={80} className="text-[#00d4ff]" />
        </div>
        <h3 className="text-[#00d4ff] text-xs font-black tracking-[0.2em] uppercase mb-4 flex items-center gap-2">
          <Quote size={14} /> Investment Thesis
        </h3>
        <p className="text-2xl font-light text-slate-100 leading-tight font-serif italic">
          "{sections.thesis}"
        </p>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Catalysts */}
        <section className="glass p-6 rounded-2xl border-l-4 border-l-[#00ff88]">
          <h3 className="text-[#00ff88] text-xs font-black tracking-[0.2em] uppercase mb-6 flex items-center gap-2">
            <Zap size={14} /> Core Catalysts
          </h3>
          <ul className="space-y-4">
            {sections.catalysts.map((item, i) => (
              <li key={i} className="flex gap-3 text-slate-300 text-sm leading-relaxed">
                <span className="text-[#00ff88] font-bold">0{i+1}.</span>
                {item}
              </li>
            ))}
          </ul>
        </section>

        {/* Risks */}
        <section className="glass p-6 rounded-2xl border-l-4 border-l-[#ff3366]">
          <h3 className="text-[#ff3366] text-xs font-black tracking-[0.2em] uppercase mb-6 flex items-center gap-2">
            <AlertTriangle size={14} /> Risk Vectors
          </h3>
          <ul className="space-y-4">
            {sections.risks.map((item, i) => (
              <li key={i} className="flex gap-3 text-slate-300 text-sm leading-relaxed">
                <span className="text-[#ff3366] font-bold">!</span>
                {item}
              </li>
            ))}
          </ul>
        </section>
      </div>

      {/* Technical Confluence */}
      <section className="glass p-6 rounded-2xl">
        <h3 className="text-slate-400 text-xs font-black tracking-[0.2em] uppercase mb-4 flex items-center gap-2">
          <GitMerge size={14} /> Technical Confluence
        </h3>
        <p className="text-slate-300 text-sm leading-relaxed font-mono bg-slate-900/50 p-4 rounded border border-slate-800">
          {sections.confluence}
        </p>
      </section>

      {/* Citations */}
      <section>
        <h3 className="text-slate-500 text-[10px] font-black tracking-[0.3em] uppercase mb-4 text-center">
          Data Citations & Sources
        </h3>
        <div className="flex flex-wrap justify-center gap-3">
          {(report.citations || []).map((cite: any, i: number) => (
            <a 
              key={i} 
              href={cite.link} 
              target="_blank" 
              className="px-3 py-1 bg-slate-900/80 border border-slate-800 rounded-full text-[10px] text-slate-400 hover:text-[#00d4ff] hover:border-[#00d4ff] transition-all flex items-center gap-2"
            >
              <LinkIcon size={10} />
              {cite.source} <span className="opacity-30">|</span> {cite.type}
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
