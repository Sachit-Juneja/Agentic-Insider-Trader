"use client";

import { useState, useRef, useEffect } from "react";
import { Search, Activity, ShieldAlert, Cpu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AgentGrid } from "@/components/terminal/AgentGrid";
import { GaugeChart } from "@/components/scorecard/GaugeChart";
import { InsiderMoves } from "@/components/deep-dive/InsiderMoves";
import { FlowAnalysis } from "@/components/deep-dive/FlowAnalysis";
import { FundamentalHealth } from "@/components/deep-dive/FundamentalHealth";
import { AgentStatus, FinalReport } from "@/lib/types";

export default function Home() {
  const [ticker, setTicker] = useState("");
  const [holdPeriod, setHoldPeriod] = useState([90]); // 90 days default
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  const [statuses, setStatuses] = useState<AgentStatus[]>([]);
  const [report, setReport] = useState<FinalReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  const eventSourceRef = useRef<EventSource | null>(null);

  const holdPeriodMap: Record<number, string> = {
    1: "1d",
    7: "1w",
    30: "1m",
    90: "3m",
    180: "6m",
    365: "1y",
  };

  const startAnalysis = async () => {
    if (!ticker) return;
    
    setIsAnalyzing(true);
    setStatuses([]);
    setReport(null);
    setError(null);

    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker,
          hold_period: holdPeriodMap[holdPeriod[0]],
          risk_tolerance: "moderate",
        }),
      });

      if (!response.ok) throw new Error("Failed to start analysis");
      
      const data = await response.json();
      const jobId = data.job_id;

      // Start SSE connection
      const es = new EventSource(`http://localhost:8000/api/analyze/${jobId}/stream`);
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

      es.onerror = () => {
        setError("Connection lost. Analysis may still be running.");
        setIsAnalyzing(false);
        es.close();
      };

    } catch (err: any) {
      setError(err.message);
      setIsAnalyzing(false);
    }
  };

  // Cleanup SSE
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) eventSourceRef.current.close();
    };
  }, []);

  return (
    <main className="container mx-auto p-4 min-h-screen flex flex-col gap-6 font-mono">
      
      {/* Header */}
      <header className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <Activity className="text-[#00d4ff] h-8 w-8" />
          <div>
            <h1 className="text-2xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-[#00d4ff] to-[#00ff88]">
              AGENTIC INSIDER TRADER
            </h1>
            <p className="text-xs text-slate-500 tracking-widest uppercase">16-Agent Intelligence Swarm</p>
          </div>
        </div>
        <Badge variant="outline" className="bg-[#0a0e27] text-[#00d4ff] border-[#00d4ff] animate-pulse">
          SYSTEM ONLINE
        </Badge>
      </header>

      {/* Control Panel */}
      <section className="bg-[#0d1333] border border-slate-800 rounded-lg p-6 shadow-2xl">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-end">
          <div className="md:col-span-3 space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase">Target Ticker</label>
            <div className="relative">
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-slate-500" />
              <Input 
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                placeholder="AAPL, TSLA, NVDA..."
                className="pl-10 bg-[#0a0e27] border-slate-700 text-lg uppercase font-bold focus-visible:ring-[#00d4ff]"
                onKeyDown={(e) => e.key === 'Enter' && startAnalysis()}
              />
            </div>
          </div>
          
          <div className="md:col-span-6 space-y-4 px-4">
            <div className="flex justify-between items-center">
              <label className="text-xs font-bold text-slate-400 uppercase">Holding Period</label>
              <span className="text-sm font-bold text-[#00ff88]">{holdPeriod[0]} Days</span>
            </div>
            <Slider
              value={holdPeriod}
              onValueChange={(value) => setHoldPeriod(value as number[])}
              max={365}
              min={1}
              step={1}
              className="py-2 [&_[role=slider]]:bg-[#00ff88] [&_[role=slider]]:border-[#00ff88]"
            />
          </div>

          <div className="md:col-span-3">
            <Button 
              onClick={startAnalysis}
              disabled={isAnalyzing || !ticker}
              className="w-full bg-[#00d4ff] hover:bg-[#00b0d4] text-[#0a0e27] font-black tracking-widest h-12 text-lg glow-primary transition-all uppercase"
            >
              {isAnalyzing ? (
                <><Cpu className="mr-2 h-5 w-5 animate-spin" /> Computing</>
              ) : (
                "Summon Swarm"
              )}
            </Button>
          </div>
        </div>
        {error && (
          <div className="mt-4 p-3 bg-red-900/20 border border-red-500/50 rounded flex items-center gap-2 text-red-400 text-sm">
            <ShieldAlert className="h-4 w-4" /> {error}
          </div>
        )}
      </section>

      {/* Terminal View / Results */}
      <section className="flex-1 border border-slate-800 rounded-lg bg-[#0a0e27]/50 backdrop-blur-xl overflow-hidden flex flex-col">
        <div className="bg-[#0d1333] border-b border-slate-800 p-2 px-4 flex items-center justify-between">
          <div className="flex gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
          </div>
          <span className="text-xs text-slate-500">Terminal — {ticker || "Awaiting Input"}</span>
        </div>

        <div className="flex-1 overflow-y-auto">
          {(!report && !isAnalyzing && statuses.length === 0) ? (
            <div className="flex flex-col items-center justify-center h-full text-slate-600 space-y-4 p-20">
              <Cpu className="h-24 w-24 opacity-20" />
              <p className="tracking-widest uppercase text-sm">Ready to analyze market vectors</p>
            </div>
          ) : (
            <Tabs defaultValue="swarm" className="w-full flex flex-col h-full">
              <div className="border-b border-slate-800 px-4 py-2 bg-[#0a0e27]">
                <TabsList className="bg-[#0d1333] border border-slate-800">
                  <TabsTrigger value="swarm" className="data-[state=active]:bg-[#00d4ff] data-[state=active]:text-[#0a0e27] font-bold">Swarm Grid</TabsTrigger>
                  <TabsTrigger value="scorecard" disabled={!report} className="data-[state=active]:bg-[#00ff88] data-[state=active]:text-[#0a0e27] font-bold">Scorecard</TabsTrigger>
                  <TabsTrigger value="insider" disabled={!report} className="data-[state=active]:bg-[#ffaa00] data-[state=active]:text-[#0a0e27] font-bold">Insider Moves</TabsTrigger>
                  <TabsTrigger value="flow" disabled={!report} className="data-[state=active]:bg-[#ff6b35] data-[state=active]:text-[#0a0e27] font-bold">Flow Analysis</TabsTrigger>
                  <TabsTrigger value="fundamentals" disabled={!report} className="data-[state=active]:bg-[#ff3366] data-[state=active]:text-[#0a0e27] font-bold">Fundamentals</TabsTrigger>
                  <TabsTrigger value="raw" disabled={!report} className="data-[state=active]:bg-slate-200 data-[state=active]:text-[#0a0e27] font-bold">Raw JSON</TabsTrigger>
                </TabsList>
              </div>

              <div className="flex-1 overflow-y-auto p-4">
                <TabsContent value="swarm" className="m-0 h-full">
                  <AgentGrid statuses={statuses} />
                </TabsContent>

                <TabsContent value="scorecard" className="m-0 h-full">
                  {report && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="col-span-1 bg-[#0d1333] p-6 rounded-lg border border-slate-800 flex flex-col items-center justify-center">
                        <GaugeChart score={report.final_score} />
                        <h2 className="text-3xl font-black mt-4" style={{
                          color: report.final_rating.includes("BUY") ? "#00ff88" : 
                                 report.final_rating.includes("SELL") ? "#ff3366" : "#ffaa00"
                        }}>
                          {report.final_rating}
                        </h2>
                      </div>
                      <div className="col-span-1 md:col-span-2 bg-[#0d1333] p-6 rounded-lg border border-slate-800">
                        <h3 className="text-[#00d4ff] font-bold uppercase mb-4 border-b border-slate-800 pb-2">Grand Synthesizer Verdict</h3>
                        <p className="text-slate-300 leading-relaxed font-sans">
                          {report.final_summary}
                        </p>
                        
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
                          <MetricCard label="Kelly Fraction" value={`${(report.risk_metrics?.kelly_fraction * 100).toFixed(1)}%`} />
                          <MetricCard label="Pos Size ($100k)" value={`$${report.risk_metrics?.position_size?.toLocaleString()}`} />
                          <MetricCard label="Est Sharpe" value={report.risk_metrics?.sharpe_ratio} />
                          <MetricCard label="Form 4 Filings" value={report.insider_highlights?.form4_count} />
                        </div>
                      </div>
                    </div>
                  )}
                </TabsContent>

                <TabsContent value="insider" className="m-0 h-full">
                  {report && <InsiderMoves report={report} />}
                </TabsContent>

                <TabsContent value="flow" className="m-0 h-full">
                  {report && <FlowAnalysis report={report} />}
                </TabsContent>

                <TabsContent value="fundamentals" className="m-0 h-full">
                  {report && <FundamentalHealth report={report} />}
                </TabsContent>

                <TabsContent value="raw" className="m-0 h-full">
                  <pre className="bg-[#050814] p-6 rounded-lg border border-slate-800 text-xs text-emerald-400 overflow-auto h-[600px] font-mono leading-relaxed">
                    {JSON.stringify(report, null, 2)}
                  </pre>
                </TabsContent>
              </div>
            </Tabs>
          )}
        </div>
      </section>
    </main>
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
