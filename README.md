# Problem Statement
Large product assortments and continuosly changing consumenr demand create significant scalability challenges for traditional deman forecasting methods. Therefore, there is a need for a solution that minimizes uncertainty and helps prevent the costly consequences that arise from ineffective inventory optimization. 

# Proposed Solution
An AI-powered forecasting system combining Streamlit frontend, agentic AI orchestration (LangChain/LlamaIndex), and Prophet forecasting integrated with PostgreSQL data.

## Agentic Forecasting System Architecture & Workflow


### System Architecture



                                User
                                │
                                ▼
                        Streamlit Frontend
                                │
                                ▼
                        Agentic AI Orchestrator
                        (LangChain / LlamaIndex)
                                │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                Forecasting Tool     Data Tool
                (Prophet model)      (SQL Query)

                    ▼                   ▼
                Forecast Model       PostgreSQL DB
                                        (Dataset)

### Workflow



                           User Prompt
                                ↓
                        Agent interprets prompt
                                ↓
                    Agent calls forecasting tool
                                ↓
                    Tool queries database
                                ↓
                    Forecast model runs
                                ↓
                    Agent summarizes result
                                ↓
                    Streamlit displays answer + chart

