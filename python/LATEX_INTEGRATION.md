# LaTeX Integration Guide

## Using the Generated Tables and Figures in Your Research Paper

### Prerequisites

Add these packages to your LaTeX preamble:

```latex
\usepackage{graphicx}  % For including images
\usepackage{csvsimple} % For CSV tables
\usepackage{booktabs}  % For professional tables
\usepackage{caption}   % For captions
\usepackage{subcaption} % For subfigures
```

---

## Tables

### Method 1: CSV Auto-Import (Recommended)

```latex
\begin{table}[ht]
\centering
\caption{UK (.co.uk) Multi-hop Coverage and TTFI Analysis}
\label{tab:uk_multihop}
\csvautotabular{output/uk_multi_hop_results.csv}
\end{table}

\begin{table}[ht]
\centering
\caption{SE (.se) Multi-hop Coverage and TTFI Analysis}
\label{tab:se_multihop}
\csvautotabular{output/se_multi_hop_results.csv}
\end{table}
```

### Method 2: Professional Formatting with csvsimple

```latex
\begin{table}[ht]
\centering
\caption{UK (.co.uk) Multi-hop Coverage and TTFI Analysis}
\label{tab:uk_multihop}
\csvreader[
    tabular=lrrrr,
    table head=\toprule
        \textbf{Country} & \textbf{Seeds} & 
        \textbf{Coverage 5-hop (\%)} & \textbf{TTFI 5-hop (s)} & 
        \textbf{Coverage 10-hop (\%)} & \textbf{TTFI 10-hop (s)} \\
        \midrule,
    table foot=\bottomrule
]{output/uk_multi_hop_results.csv}
{Country=\country, Seeds=\seeds, Coverage_5hop_%=\covfive, 
 TTFI_5hop_s=\ttfifive, Coverage_10hop_%=\covten, TTFI_10hop_s=\ttfiten}
{\country & \seeds & \covfive & \ttfifive & \covten & \ttfiten}
\end{table}
```

### Method 3: Side-by-Side Comparison

```latex
\begin{table}[ht]
\centering
\caption{Multi-hop Coverage Comparison: UK vs SE}
\label{tab:multihop_comparison}
\begin{subtable}[t]{0.48\textwidth}
    \centering
    \caption{UK (.co.uk)}
    \csvautotabular{output/uk_multi_hop_results.csv}
\end{subtable}
\hfill
\begin{subtable}[t]{0.48\textwidth}
    \centering
    \caption{SE (.se)}
    \csvautotabular{output/se_multi_hop_results.csv}
\end{subtable}
\end{table}
```

---

## Figures

### Single Figure

```latex
\begin{figure}[ht]
\centering
\includegraphics[width=0.8\textwidth]{output/figure7_coverage_vs_seeds_se_vs_uk.png}
\caption{Coverage vs seed sites: .co.uk vs .se domains}
\label{fig:coverage_comparison}
\end{figure}
```

### Figure with Different Widths

```latex
% Full width for detailed graphs
\begin{figure}[ht]
\centering
\includegraphics[width=\textwidth]{output/figure6_ttfi_vs_seeds_couk.png}
\caption{TTFI vs number of seed sites for .co.uk domains}
\label{fig:ttfi_couk}
\end{figure}

% Half width for simpler graphs
\begin{figure}[ht]
\centering
\includegraphics[width=0.5\textwidth]{output/figure1_couk_active_share.png}
\caption{.co.uk domain counts and active share}
\label{fig:couk_active}
\end{figure}
```

### Subfigures (2x2 Grid)

```latex
\begin{figure}[ht]
\centering
\begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{output/figure2_twohop_seeds_vs_coverage_43.png}
    \caption{Two-hop model}
    \label{fig:twohop}
\end{subfigure}
\hfill
\begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{output/figure4_threehop_seeds_vs_coverage_43.png}
    \caption{Three-hop model}
    \label{fig:threehop}
\end{subfigure}
\\[1em]
\begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{output/uk_co_uk_multi_hop_coverage.png}
    \caption{UK multi-hop coverage}
    \label{fig:uk_multihop}
\end{subfigure}
\hfill
\begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{output/se_se_multi_hop_coverage.png}
    \caption{SE multi-hop coverage}
    \label{fig:se_multihop}
\end{subfigure}
\caption{Coverage analysis across different hop models and TLDs}
\label{fig:coverage_analysis}
\end{figure}
```

### All 8 Paper Figures

```latex
% Figure 1: Active domains
\begin{figure}[ht]
\centering
\includegraphics[width=0.6\textwidth]{output/figure1_couk_active_share.png}
\caption{.co.uk domain counts and active share estimates}
\label{fig:couk_active}
\end{figure}

% Figure 2: Two-hop seeds vs coverage
\begin{figure}[ht]
\centering
\includegraphics[width=0.8\textwidth]{output/figure2_twohop_seeds_vs_coverage_43.png}
\caption{Two-hop model: seeds required vs coverage for .co.uk (43\% active)}
\label{fig:twohop_coverage}
\end{figure}

% Figure 3: Active share comparison
\begin{figure}[ht]
\centering
\includegraphics[width=0.7\textwidth]{output/figure3_seeds_90pct_active_share.png}
\caption{Seeds required at 90\% coverage: 43\% vs 50\% active share}
\label{fig:active_share_comparison}
\end{figure}

% Figure 4: Three-hop model
\begin{figure}[ht]
\centering
\includegraphics[width=0.8\textwidth]{output/figure4_threehop_seeds_vs_coverage_43.png}
\caption{Three-hop model: seeds required vs coverage for .co.uk (43\% active)}
\label{fig:threehop_coverage}
\end{figure}

% Figure 5: Two vs three hop comparison
\begin{figure}[ht]
\centering
\includegraphics[width=0.7\textwidth]{output/figure5_seeds_90pct_two_vs_three_hops.png}
\caption{Seeds at 90\% coverage: two-hop vs three-hop models}
\label{fig:hop_comparison}
\end{figure}

% Figure 6: TTFI analysis
\begin{figure}[ht]
\centering
\includegraphics[width=0.8\textwidth]{output/figure6_ttfi_vs_seeds_couk.png}
\caption{Time To First Index vs number of seed sites (.co.uk baseline)}
\label{fig:ttfi_baseline}
\end{figure}

% Figure 7: Coverage SE vs UK
\begin{figure}[ht]
\centering
\includegraphics[width=0.85\textwidth]{output/figure7_coverage_vs_seeds_se_vs_uk.png}
\caption{Two-hop coverage vs seed sites: .co.uk vs .se comparison}
\label{fig:coverage_tld_comparison}
\end{figure}

% Figure 8: TTFI SE vs UK
\begin{figure}[ht]
\centering
\includegraphics[width=0.85\textwidth]{output/figure8_ttfi_vs_seeds_se_vs_uk.png}
\caption{TTFI vs seed sites: .co.uk vs .se comparison}
\label{fig:ttfi_tld_comparison}
\end{figure}
```

---

## Cross-Referencing

In your text, reference tables and figures like this:

```latex
As shown in Table~\ref{tab:uk_multihop}, the UK .co.uk domain 
requires significantly more seed sites than the SE .se domain 
(Table~\ref{tab:se_multihop}) to achieve equivalent coverage.

Figure~\ref{fig:coverage_comparison} illustrates the relationship 
between seed site count and domain coverage across both TLDs.

The TTFI analysis (Figure~\ref{fig:ttfi_baseline}) demonstrates 
that increasing seed sites from 5,000 to 50,000 reduces discovery 
latency by approximately 30\%.
```

---

## Complete Example Section

```latex
\section{Multi-hop Coverage Analysis}

\subsection{Model Parameters and Setup}

Our analysis uses the following baseline parameters:
\begin{itemize}
    \item Effective out-degree: $D = 10.37$
    \item Second-hop deduplication: $r = 0.6$
    \item Third+ hop deduplication: $s = 0.45$
    \item Cross-seed overlap: $\theta = 0.3$
    \item Latency per hop: $\tau_{hop} = 3.0$ seconds
\end{itemize}

\subsection{Results}

Table~\ref{tab:uk_multihop} presents the multi-hop coverage and TTFI 
results for UK .co.uk domains across different seed configurations.

\begin{table}[ht]
\centering
\caption{UK (.co.uk) Multi-hop Coverage and TTFI Analysis}
\label{tab:uk_multihop}
\csvreader[
    tabular=lrrrr,
    table head=\toprule
        \textbf{Country} & \textbf{Seeds} & 
        \textbf{5-hop Cov. (\%)} & \textbf{5-hop TTFI (s)} & 
        \textbf{10-hop Cov. (\%)} & \textbf{10-hop TTFI (s)} \\
        \midrule,
    table foot=\bottomrule
]{output/uk_multi_hop_results.csv}
{Country=\country, Seeds=\seeds, Coverage_5hop_%=\covfive, 
 TTFI_5hop_s=\ttfifive, Coverage_10hop_%=\covten, TTFI_10hop_s=\ttfiten}
{\country & \seeds & \covfive & \ttfifive & \covten & \ttfiten}
\end{table}

Figure~\ref{fig:multihop_comparison} shows the coverage evolution 
across different hop depths.

\begin{figure}[ht]
\centering
\begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{output/uk_co_uk_multi_hop_coverage.png}
    \caption{UK coverage}
    \label{fig:uk_multihop_cov}
\end{subfigure}
\hfill
\begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{output/uk_co_uk_multi_hop_ttfi.png}
    \caption{UK TTFI}
    \label{fig:uk_multihop_ttfi}
\end{subfigure}
\caption{UK multi-hop analysis: 5 vs 10 hop comparison}
\label{fig:multihop_comparison}
\end{figure}

\subsection{Discussion}

Our results indicate that...
```

---

## Tips for Publication Quality

1. **Image Resolution**: All figures are generated at 300 DPI, suitable for publication
2. **Consistent Sizing**: Use consistent width values (e.g., 0.8\textwidth) for similar figures
3. **Caption Placement**: 
   - Tables: Caption at top (`\caption` before content)
   - Figures: Caption at bottom (`\caption` after content)
4. **Cross-references**: Always use `\label` and `\ref` instead of hard-coding numbers
5. **Float Placement**: Use `[ht]` for flexible placement, `[H]` (with `\usepackage{float}`) to force exact position

---

## Troubleshooting

### Issue: CSV table formatting is broken
**Solution**: Add column alignment in csvsimple:
```latex
\csvreader[tabular=lrrrr, ...]{file.csv}...
% l = left, r = right, c = center
```

### Issue: Images too large/small
**Solution**: Adjust width parameter:
```latex
\includegraphics[width=0.5\textwidth]{...}  % Smaller
\includegraphics[width=1.0\textwidth]{...}  % Full width
```

### Issue: Figures appear in wrong place
**Solution**: Use specific placement:
```latex
\begin{figure}[H]  % Forces exact placement (requires \usepackage{float})
\begin{figure}[!h] % Strongly prefers here
\begin{figure}[tb] % Top or bottom only
```

---

## Complete LaTeX Preamble

```latex
\documentclass[11pt,a4paper]{article}

% Packages for tables and figures
\usepackage{graphicx}
\usepackage{csvsimple}
\usepackage{booktabs}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{float}

% Path to output directory
\graphicspath{{output/}}

\begin{document}

% Your content here

\end{document}
```
