"use client";

import { useState, useRef, useEffect } from "react";
import { Search, Activity, ShieldAlert, Cpu, BarChart4, TrendingUp, History, Database } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AgentGrid } from "@/components/terminal/AgentGrid";
import { GaugeChart } from "@/components/scorecard/GaugeChart";
import { DeepReport } from "@/components/scorecard/DeepReport";
import { InsiderMoves } from "@/components/deep-dive/InsiderMoves";
import { FlowAnalysis } from "@/components/deep-dive/FlowAnalysis";
import { FundamentalHealth } from "@/components/deep-dive/FundamentalHealth";
import { AgentStatus, FinalReport } from "@/lib/types";

export default function Home() {
  const [ticker, setTicker] = useState("");
  const [holdPeriodIdx, setHoldPeriodIdx] = useState([3]); // index in holdPeriods array
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [statuses, setStatuses] = useState<AgentStatus[]>([]);
  const [report, setReport] = useState<FinalReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  const eventSourceRef = useRef<EventSource | null>(null);

  const holdPeriods = [
    { label: "1 Day", val: "1d" },
    { label: "1 Week", val: "1w" },
    { label: "1 Month", val: "1m" },
    { label: "3 Months", val: "3m" },
    { label: "6 Months", val: "6m" },
    { label: "1 Year", val: "1y" },
  ];

  const startAnalysis = async () => {
    if (!ticker) return;
    setIsAnalyzing(true);
    setStatuses([]);
    setReport(null);
    setError(null);

    if (eventSourceRef.current) eventSourceRef.current.close();

    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker,
          hold_period: holdPeriods[holdPeriodIdx[0]].val,
          risk_tolerance: "moderate",
        }),
      });

      if (!response.ok) throw new Error("Failed to start analysis");
      const data = await response.json();
      const es = new EventSource(`http://localhost:8000/api/analyze/${data.job_id}/stream`);
      eventSourceRef.current = es;

      es.onmessage = (event) => {
        const parsed = JSON.parse(event.data);
        if (parsed.type === "agent_status") {
          setStatuses((prev) => {
            const newStatuses = [...prev];
            const idx = newStatuses.findIndex(s => s.agent_name === parsed.data.agent_name);
            if (idx >= 0) newStatuses[idx] = parsed.data;
            else newStatuses.push(parsed.data);
            return newStatuses;
          });
        } else if (parsed.type === "complete") {
          setReport(parsed.data);
          setIsAnalyzing(false);
          es.close();
        } else if (parsed.type === "error") {
          setError(parsed.data.error);
          setIsAnalyzing(false);
          es.close();
        }
      };
    } catch (err: any) {
      setError(err.message);
      setIsAnalyzing(false);
    }
  };

  useEffect(() => {
    return () => { if (eventSourceRef.current) eventSourceRef.current.close(); };
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-200">
      
      {/* Navigation */}
      <nav className="h-16 border-b border-slate-800/50 flex items-center justify-between px-8 glass sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <Activity className="text-[#00d4ff] h-6 w-6 glow-primary" />
          <h1 className="text-lg font-black tracking-widest text-white uppercase glow-text">
            Agentic Insider <span className="text-[#00d4ff]">Trader</span>
          </h1>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
            <Database size={12} className="text-emerald-500" /> API: Production
          </div>
          <Badge variant="outline" className="bg-[#00d4ff]/10 text-[#00d4ff] border-[#00d4ff]/30 text-[10px] font-bold py-0.5">
            16 AGENTS ACTIVE
          </Badge>
        </div>
      </nav>

      <main className="flex-1 flex flex-col max-w-7xl mx-auto w-full p-8 gap-8">
        
        {/* Search & Parameters Section */}
        <div className="glass p-8 rounded-3xl grid grid-cols-1 md:grid-cols-12 gap-12 items-center">
          <div className="md:col-span-4 space-y-3">
            <label className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Asset Identifier</label>
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-500" />
              <Input 
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                placeholder="TICKER"
                className="pl-12 h-14 bg-slate-900/50 border-slate-800 text-xl font-bold tracking-widest uppercase rounded-2xl focus-visible:ring-[#00d4ff]"
                onKeyDown={(e) => e.key === 'Enter' && startAnalysis()}
              />
            </div>
          </div>

          <div className="md:col-span-5 space-y-4">
            <div className="flex justify-between items-end">
              <label className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Strategy Horizon</label>
              <span className="text-sm font-black text-[#00ff88]">{holdPeriods[holdPeriodIdx[0]].label}</span>
            </div>
            <Slider
              value={holdPeriodIdx}
              onValueChange={(value) => setHoldPeriodIdx(value as number[])}
              max={holdPeriods.length - 1}
              min={0}
              step={1}
              className="py-2"
            />
          </div>

          <div className="md:col-span-3">
            <Button 
              onClick={startAnalysis}
              disabled={isAnalyzing || !ticker}
              className="w-full h-14 bg-[#00d4ff] hover:bg-[#00d4ff]/80 text-slate-950 font-black tracking-widest text-sm transition-all uppercase rounded-2xl shadow-[0_0_30px_rgba(0,212,255,0.2)] active:scale-95"
            >
              {isAnalyzing ? (
                <><Cpu className="mr-2 h-5 w-5 animate-spin" /> Computing...</>
              ) : (
                "Initiate Analysis"
              )}
            </Button>
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-900/10 border border-red-500/30 rounded-2xl flex items-center gap-3 text-red-400 text-sm animate-in fade-in zoom-in-95">
            <ShieldAlert className="h-4 w-4" /> {error}
          </div>
        )}

        {/* Dashboard Content */}
        {(!report && !isAnalyzing && statuses.length === 0) ? (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-700 min-h-[400px]">
            <div className="relative mb-8">
              <BarChart4 className="h-32 w-32 opacity-10" />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950 to-transparent" />
            </div>
            <p className="text-xs font-black tracking-[0.4em] uppercase opacity-40">System Standby // Awaiting Signal</p>
          </div>
        ) : (
          <div className="flex-1 flex flex-col gap-8 animate-in fade-in duration-700">
            
            <Tabs defaultValue="report" className="w-full">
              <div className="flex items-center justify-between mb-8 border-b border-slate-800 pb-2">
                <TabsList className="bg-transparent h-auto p-0 gap-8">
                  <TabsTrigger value="report" disabled={!report} className="dashboard-tab">Executive Report</TabsTrigger>
                  <TabsTrigger value="swarm" className="dashboard-tab">Swarm Intelligence</TabsTrigger>
                  <TabsTrigger value="insider" disabled={!report} className="dashboard-tab">Insider Flow</TabsTrigger>
                  <TabsTrigger value="technicals" disabled={!report} className="dashboard-tab">Technicals</TabsTrigger>
                </TabsList>
                
                {report && (
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-[10px] font-bold">
                      <TrendingUp size={12} className="text-emerald-400" />
                      CONVICTION: {(report.final_score).toFixed(0)}%
                    </div>
                  </div>
                )}
              </div>

              <div className="min-h-[600px]">
                <TabsContent value="report" className="focus-visible:outline-none">
                  {report && (
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                      <div className="lg:col-span-4 space-y-8">
                        <div className="glass p-8 rounded-3xl flex flex-col items-center text-center">
                          <GaugeChart score={report.final_score} />
                          <div className="mt-8 space-y-1">
                            <div className="text-[10px] font-black text-slate-500 tracking-[0.3em] uppercase">Aggregated Rating</div>
                            <h2 className="text-4xl font-black tracking-tighter" style={{
                              color: report.final_rating.includes("BUY") ? "#00ff88" : 
                                     report.final_rating.includes("SELL") ? "#ff3366" : "#ffaa00"
                            }}>
                              {report.final_rating}
                            </h2>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4">
                          <MiniCard label="Kelly Frac" value={`${(report.risk_metrics?.kelly_fraction * 100).toFixed(1)}%`} />
                          <MiniCard label="Pos Size" value={`$${report.risk_metrics?.position_size?.toLocaleString()}`} />
                          <MiniCard label="Sharpe" value={report.risk_metrics?.sharpe_ratio} />
                          <MiniCard label="VaR (95%)" value={`$${report.risk_metrics?.var_95?.toLocaleString()}`} />
                        </div>
                      </div>

                      <div className="lg:col-span-8">
                        <DeepReport report={report} />
                      </div>
                    </div>
                  )}
                </TabsContent>

                <TabsContent value="swarm" className="focus-visible:outline-none">
                  <AgentGrid statuses={statuses} />
                </TabsContent>

                <TabsContent value="insider" className="focus-visible:outline-none">
                  {report && <InsiderMoves report={report} />}
                </TabsContent>

                <TabsContent value="technicals" className="focus-visible:outline-none">
                  {report && <FundamentalHealth report={report} />}
                </TabsContent>
              </div>
            </Tabs>
          </div>
        )}
      </main>

      {/* Footer / Status Bar */}
      <footer className="h-8 border-t border-slate-800/50 flex items-center px-8 text-[9px] font-bold text-slate-600 gap-6 uppercase tracking-widest bg-slate-950/80 backdrop-blur">
        <div className="flex items-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
          Quantum Engine: v4.5.1
        </div>
        <div>Uptime: 99.9%</div>
        <div className="ml-auto flex items-center gap-4">
          <span className="text-[#00d4ff]">Latency: 42ms</span>
          <span>© 2026 Insider Trader Swarm</span>
        </div>
      </footer>

      <style jsx global>{`
        .dashboard-tab {
          @apply text-slate-500 font-bold text-xs uppercase tracking-widest border-b-2 border-transparent px-0 pb-2 transition-all rounded-none data-[state=active]:text-white data-[state=active]:border-[#00d4ff] data-[state=active]:bg-transparent shadow-none !important;
        }
        .glass {
          background: rgba(15, 23, 42, 0.6);
          backdrop-filter: blur(12px);
          border: 1px solid rgba(255, 255, 255, 0.05);
        }
      `}</style>
    </div>
  );
}

function MiniCard({ label, value }: { label: string, value: any }) {
  return (
    <div className="glass p-4 rounded-2xl">
      <div className="text-[9px] font-black text-slate-500 tracking-widest uppercase mb-1">{label}</div>
      <div className="text-lg font-bold text-slate-100">{value || "---"}</div>
    </div>
  );
}

function MetricCard({ label, value }: { label: string, value: any }) {
  return (
    <div className="bg-[#0a0e27] p-3 rounded border border-slate-800/50">
      <div className="text-[10px] uppercase text-slate-500 font-bold mb-1">{label}</div>
      <div className="text-lg text-slate-200 font-bold">{value || "N/A"}</div>
    </div>
  );
}
