export interface AgentStatus {
  agent_name: string;
  status: "pending" | "running" | "complete" | "error";
  summary: string;
  confidence: number;
  execution_time_ms: number;
}

export interface FinalReport {
  ticker: string;
  hold_period: string;
  final_score: number;
  final_rating: string;
  final_summary: string;
  gauge_config: any;
  agent_breakdown: any[];
  risk_metrics: any;
  insider_highlights: any;
  flow_analysis: any;
  technical_charts: any;
  timestamp: string;
}
