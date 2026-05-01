"use client";

import { motion } from "framer-motion";
import { AgentStatus } from "@/lib/types";
import { Loader2, CheckCircle2, XCircle, Clock } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

// Order of agents as defined in backend
const AGENT_ROSTER = [
  "user_proxy",
  "macro_agent",
  "geopolitical_agent",
  "market_regime_agent",
  "technical_analyst",
  "options_flow_agent",
  "dark_pool_monitor",
  "fundamental_agent",
  "sector_comparator",
  "insider_trading_agent",
  "media_sentiment_agent",
  "social_scraper",
  "risk_optimization_agent",
  "grand_synthesizer",
  "report_generator",
];

const AGENT_DISPLAY_NAMES: Record<string, string> = {
  user_proxy: "User Proxy",
  macro_agent: "Macroeconomic",
  geopolitical_agent: "Geopolitical Risk",
  market_regime_agent: "Market Regime",
  technical_analyst: "Technical Analyst",
  options_flow_agent: "Options Flow",
  dark_pool_monitor: "Dark Pool Monitor",
  fundamental_agent: "Fundamental Health",
  sector_comparator: "Sector Comparator",
  insider_trading_agent: "Insider Trading",
  media_sentiment_agent: "Media Sentiment",
  social_scraper: "Social Scraper",
  risk_optimization_agent: "Risk & Opt",
  grand_synthesizer: "Grand Synthesizer",
  report_generator: "Report Generator",
};

export function AgentGrid({ statuses }: { statuses: AgentStatus[] }) {
  const statusMap = new Map(statuses.map((s) => [s.agent_name, s]));

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
      {AGENT_ROSTER.map((agentId, index) => {
        const status = statusMap.get(agentId) || {
          agent_name: agentId,
          status: "pending",
          summary: "Awaiting signal...",
          confidence: 0,
        };

        const isRunning = status.status === "running";
        const isComplete = status.status === "complete";
        const isError = status.status === "error";

        return (
          <motion.div
            key={agentId}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: index * 0.03 }}
            className={`glass p-4 rounded-2xl flex flex-col gap-2 transition-all duration-500 ${
              isRunning ? "ring-1 ring-[#00d4ff]/50 glow-primary" : 
              isComplete ? "ring-1 ring-[#00ff88]/30" : 
              "opacity-40"
            }`}
          >
            <div className="flex justify-between items-start">
              <div className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400">
                {AGENT_DISPLAY_NAMES[agentId]}
              </div>
              {isRunning && <Loader2 size={10} className="text-[#00d4ff] animate-spin" />}
              {isComplete && <div className="w-1.5 h-1.5 rounded-full bg-[#00ff88] shadow-[0_0_5px_#00ff88]" />}
            </div>
            
            <div className="text-[10px] text-slate-500 leading-tight line-clamp-2 font-medium italic">
              {isRunning ? "Computing vectors..." : status.summary}
            </div>
            
            {isComplete && (
              <div className="mt-auto flex justify-between items-end">
                <div className="text-[8px] font-bold text-slate-600">CONF: {(status.confidence * 100).toFixed(0)}%</div>
              </div>
            )}
          </motion.div>
        );
      })}
    </div>
  );
}
