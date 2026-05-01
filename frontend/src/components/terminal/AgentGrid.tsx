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
  // Map current statuses, fallback to pending
  const statusMap = new Map(statuses.map((s) => [s.agent_name, s]));

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 p-4">
      {AGENT_ROSTER.map((agentId, index) => {
        const status = statusMap.get(agentId) || {
          agent_name: agentId,
          status: "pending",
          summary: "Waiting for dispatch...",
          confidence: 0,
          execution_time_ms: 0,
        };

        const isRunning = status.status === "running";
        const isComplete = status.status === "complete";
        const isError = status.status === "error";

        let borderClass = "border-slate-800";
        let glowClass = "";
        
        if (isRunning) {
          borderClass = "border-[#00d4ff]";
          glowClass = "glow-primary";
        } else if (isComplete) {
          borderClass = "border-[#00ff88]";
          glowClass = "glow-success";
        } else if (isError) {
          borderClass = "border-[#ff3366]";
          glowClass = "glow-danger";
        }

        return (
          <motion.div
            key={agentId}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
          >
            <Card
              className={`bg-[#0d1333] ${borderClass} ${glowClass} text-slate-300 transition-all duration-300 relative overflow-hidden h-32 flex flex-col`}
            >
              <div className="p-3 flex justify-between items-center border-b border-slate-800/50">
                <span className="text-xs font-bold text-slate-200 uppercase tracking-wider truncate">
                  {AGENT_DISPLAY_NAMES[agentId]}
                </span>
                {isRunning && <Loader2 className="h-4 w-4 text-[#00d4ff] animate-spin" />}
                {isComplete && <CheckCircle2 className="h-4 w-4 text-[#00ff88]" />}
                {isError && <XCircle className="h-4 w-4 text-[#ff3366]" />}
                {status.status === "pending" && <Clock className="h-4 w-4 text-slate-600" />}
              </div>
              
              <div className="p-3 flex-1 flex flex-col justify-center">
                {isRunning ? (
                  <div className="space-y-2">
                    <Progress value={null} className="h-1 bg-slate-800" />
                    <p className="text-[10px] text-[#00d4ff] animate-pulse uppercase tracking-widest text-center">
                      Processing...
                    </p>
                  </div>
                ) : (
                  <p className="text-[10px] text-slate-400 line-clamp-3 leading-snug">
                    {status.summary}
                  </p>
                )}
              </div>
            </Card>
          </motion.div>
        );
      })}
    </div>
  );
}
