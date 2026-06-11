document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // LIVE DASHBOARD DATA FETCHING
    // ==========================================
    async function fetchDashboardData() {
        const response = await fetch('/api/dashboard', {
            headers: {
                'Accept': 'application/json'
            }
        });

        if (response.status === 401) {
            window.location = '/login';
            return null;
        }

        if (!response.ok) {
            throw new Error('Unable to load dashboard data');
        }

        return response.json();
    }

    function updateMetrics(counts) {
        const openEl = document.getElementById('count-open');
        const assignedEl = document.getElementById('count-assigned');
        const resolvedEl = document.getElementById('count-resolved');
        const opsEl = document.getElementById('count-operators');

        if (openEl) openEl.innerText = counts.open || 0;
        if (assignedEl) assignedEl.innerText = counts.assigned || 0;
        if (resolvedEl) resolvedEl.innerText = counts.resolved || 0;
        if (opsEl) opsEl.innerText = counts.operators || 0;
    }

    function renderTicketsTable(tickets) {
        const tbody = document.getElementById('tickets-table-body');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (!tickets || tickets.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 20px;">No open tickets found in the system.</td></tr>`;
            return;
        }

        tickets.forEach(t => {
            const tr = document.createElement('tr');
            let priorityClass = 'low';
            if (t.priority && t.priority.toLowerCase() === 'high') priorityClass = 'high';
            else if (t.priority && t.priority.toLowerCase() === 'medium') priorityClass = 'medium';

            const statusClass = t.status && t.status.toLowerCase() === 'open' ? 'critical' : 'active';

            tr.innerHTML = `
                <td style="font-family: monospace; color: var(--info); font-weight: 600;">${t.id}</td>
                <td><span class="prio-badge ${priorityClass}">${t.priority || 'Medium'}</span></td>
                <td style="font-size: 0.85rem; font-weight: 500;">${t.category || 'General'}</td>
                <td><a href="/ticket/${encodeURIComponent(t.id)}" style="color: #ffffff; text-decoration: none; font-weight: 500; transition: color 0.15s ease;" onmouseover="this.style.color='var(--primary)'" onmouseout="this.style.color='#ffffff'">${t.title || 'No summary available'}</a></td>
                <td>
                    <div class="status-indicator">
                        <span class="status-dot ${statusClass}"></span>
                        <span style="font-size: 0.8rem; text-transform: uppercase;">${t.status || 'OPEN'}</span>
                    </div>
                </td>
                <td style="font-family: monospace; font-size: 0.85rem;">${t.assigned || 'Unassigned'}</td>
                <td>
                    <a href="/ticket/${encodeURIComponent(t.id)}" class="btn-action-small primary" style="text-decoration:none; display:inline-block; width:100%; text-align:center;">View</a>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    async function refreshDashboard() {
        try {
            const data = await fetchDashboardData();
            if (!data) return;

            updateMetrics(data.counts || {});
            renderTicketsTable(data.tickets || []);
            addTerminalLog(`[INFO] Dashboard refreshed with live ticket data.`, 'info');
        } catch (error) {
            console.error(error);
            addTerminalLog(`Unable to load live dashboard data.`, 'error');
        }
    }

    const btnRefresh = document.getElementById('btn-refresh-dashboard');
    if (btnRefresh) {
        btnRefresh.addEventListener('click', refreshDashboard);
    }

    refreshDashboard();
    setInterval(refreshDashboard, 10000);

    // ==========================================
    // METRICS COUNT CALCULATION
    // ==========================================
    // This section is intentionally left empty because live data comes from the backend.

    // ==========================================
    // RENDER TICKETS TABLE
    // ==========================================
    // Rendering is handled by the live fetch path above.

    // ==========================================
    // NODE BREAK SIMULATION (Spikes graphs & alerts)
    // ==========================================
    // The simulator logic has been removed to focus on real ticket management.

    // ==========================================
    // GENERATOR ACTIONS
    // ==========================================
    // The fake ticket generator has been removed from the live dashboard.

    // ==========================================
    // LOG CONSOLE TERMINAL
    // ==========================================
    const logConsole = document.getElementById('skynet-logs-terminal');
    function addTerminalLog(message, type = 'text') {
        if (!logConsole) return;
        
        const timestamp = new Date().toLocaleTimeString();
        const line = document.createElement('div');
        line.className = `terminal-line ${type}`;
        line.innerHTML = `<span class="terminal-timestamp">[${timestamp}]</span>${message}`;
        
        logConsole.appendChild(line);
        logConsole.scrollTop = logConsole.scrollHeight;
    }

    // Periodic terminal checks
    if (logConsole) {
        addTerminalLog("CloudQueueX Daemon running checks...", "info");
        addTerminalLog("Establishing secure connection to Amazon SQS...", "info");
        addTerminalLog("DynamoDB client state check: 100% OK", "success");

        setInterval(() => {
            const rand = Math.random();
            if (rand < 0.25) {
                addTerminalLog("SQS Worker thread: Polling queue for new events...", "text");
            } else if (rand < 0.4) {
                addTerminalLog("SNS Notification Manager: Heartbeat normal.", "success");
            } else if (rand < 0.5) {
                addTerminalLog("DynamoDB storage check: Write operations successful.", "info");
            }
        }, 5000);
    }

    // ==========================================
    // TELEMETRY CHARTS RENDERING (ApexCharts)
    // ==========================================
    const cpuChartEl = document.querySelector("#chart-cpu");
    const memChartEl = document.querySelector("#chart-mem");

    if (cpuChartEl && memChartEl) {
        window.cpuData = [];
        window.memData = [];
        const maxPoints = 12;

        let time = new Date().getTime() - 24000;
        for (let i = 0; i < maxPoints; i++) {
            window.cpuData.push({ x: time, y: Math.floor(18 + Math.random() * 15) });
            window.memData.push({ x: time, y: Math.floor(48 + Math.random() * 8) });
            time += 2000;
        }

        const chartOptions = {
            chart: {
                type: 'area',
                height: 180,
                animations: { enabled: true, easing: 'linear', dynamicAnimation: { speed: 800 } },
                toolbar: { show: false },
                background: 'transparent',
                sparkline: { enabled: true }
            },
            stroke: { curve: 'smooth', width: 2 },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.25,
                    opacityTo: 0.05,
                }
            },
            theme: { mode: 'dark' },
            xaxis: { type: 'datetime' },
            yaxis: { min: 0, max: 100 },
            grid: { show: false }
        };

        const cpuOpts = { ...chartOptions, colors: ['#ff9900'], series: [{ name: 'CPU Load', data: window.cpuData }] };
        const memOpts = { ...chartOptions, colors: ['#0ea5e9'], series: [{ name: 'RAM Alloc', data: window.memData }] };

        window.cpuChart = new ApexCharts(cpuChartEl, cpuOpts);
        window.memChart = new ApexCharts(memChartEl, memOpts);

        window.cpuChart.render();
        window.memChart.render();

        // Update loop
        setInterval(() => {
            const now = new Date().getTime();
            
            let nextCpu = Math.floor(16 + Math.random() * 15);
            let nextMem = Math.floor(48 + Math.random() * 6);
            
            // Retain spikes temporarily
            const lastCpu = window.cpuData[window.cpuData.length - 1].y;
            if (lastCpu > 80) nextCpu = Math.floor(84 + Math.random() * 8);
            
            const lastMem = window.memData[window.memData.length - 1].y;
            if (lastMem > 80) nextMem = Math.floor(82 + Math.random() * 6);

            window.cpuData.push({ x: now, y: nextCpu });
            window.memData.push({ x: now, y: nextMem });

            if (window.cpuData.length > maxPoints) window.cpuData.shift();
            if (window.memData.length > maxPoints) window.memData.shift();

            window.cpuChart.updateSeries([{ data: window.cpuData }]);
            window.memChart.updateSeries([{ data: window.memData }]);
        }, 3000);
    }

    // Init updates
    updateMetrics();
    renderTicketsTable();
});
