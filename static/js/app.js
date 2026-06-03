document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // SEED INITIAL TICKETS IF NOT PRESENT
    // ==========================================
    const defaultTickets = [
        {
            id: "#1001",
            priority: "High",
            category: "Service",
            title: "SSH service down on practice server",
            status: "open",
            assigned: "operator01",
            score: 0
        },
        {
            id: "#1002",
            priority: "Medium",
            category: "Firewall",
            title: "Security group block on API port",
            status: "open",
            assigned: "operator02",
            score: 0
        }
    ];

    function getTickets() {
        const stored = localStorage.getItem('cqx_tickets');
        if (!stored) {
            localStorage.setItem('cqx_tickets', JSON.stringify(defaultTickets));
            return defaultTickets;
        }
        return JSON.parse(stored);
    }

    function saveTickets(tickets) {
        localStorage.setItem('cqx_tickets', JSON.stringify(tickets));
    }

    // ==========================================
    // METRICS COUNT CALCULATION
    // ==========================================
    function updateMetrics() {
        const tickets = getTickets();
        
        let openCount = 0;
        let assignedCount = 0;
        let resolvedCount = 0;
        
        tickets.forEach(t => {
            const s = t.status.toLowerCase();
            if (s === 'open') openCount++;
            else if (s === 'assigned') assignedCount++;
            else if (s === 'resolved') resolvedCount++;
        });

        const openEl = document.getElementById('count-open');
        const assignedEl = document.getElementById('count-assigned');
        const resolvedEl = document.getElementById('count-resolved');
        const opsEl = document.getElementById('count-operators');

        if (openEl) openEl.innerText = openCount;
        if (assignedEl) assignedEl.innerText = assignedCount;
        if (resolvedEl) resolvedEl.innerText = resolvedCount;
        if (opsEl) opsEl.innerText = "10"; 
    }

    // ==========================================
    // RENDER TICKETS TABLE
    // ==========================================
    function renderTicketsTable() {
        const tbody = document.getElementById('tickets-table-body');
        if (!tbody) return;

        const tickets = getTickets();
        tbody.innerHTML = '';

        if (tickets.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 20px;">No incidents currently reported in queue.</td></tr>`;
            return;
        }

        tickets.forEach(t => {
            const tr = document.createElement('tr');
            
            // Priority badge styling matching style.css
            let priorityClass = 'low';
            if (t.priority.toLowerCase() === 'high') priorityClass = 'high';
            else if (t.priority.toLowerCase() === 'medium') priorityClass = 'medium';

            tr.innerHTML = `
                <td style="font-family: monospace; color: var(--info); font-weight: 600;">${t.id}</td>
                <td><span class="prio-badge ${priorityClass}">${t.priority}</span></td>
                <td style="font-size: 0.85rem; font-weight: 500;">${t.category}</td>
                <td><a href="/ticket-demo" style="color: #ffffff; text-decoration: none; font-weight: 500; transition: color 0.15s ease;" onmouseover="this.style.color='var(--primary)'" onmouseout="this.style.color='#ffffff'">${t.title}</a></td>
                <td>
                    <div class="status-indicator">
                        <span class="status-dot ${t.status.toLowerCase() === 'open' ? 'critical' : 'active'}"></span>
                        <span style="font-size: 0.8rem; text-transform: uppercase;">${t.status}</span>
                    </div>
                </td>
                <td style="font-family: monospace; font-size: 0.85rem;">${t.assigned || '-'}</td>
                <td>
                    <button class="btn-action-small danger btn-break-machine" data-id="${t.id}">Break Node</button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        // Attach break machine simulator
        document.querySelectorAll('.btn-break-machine').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const ticketId = e.target.getAttribute('data-id');
                triggerMachineBreak(ticketId);
            });
        });
    }

    // ==========================================
    // NODE BREAK SIMULATION (Spikes graphs & alerts)
    // ==========================================
    function triggerMachineBreak(ticketId) {
        if (window.cpuChart && window.memChart) {
            const time = new Date().getTime();
            window.cpuData.push({ x: time, y: 97 });
            window.memData.push({ x: time, y: 94 });
            window.cpuChart.updateSeries([{ data: window.cpuData }]);
            window.memChart.updateSeries([{ data: window.memData }]);
        }

        // Post critical warnings to console logs
        addTerminalLog(`[CRITICAL] System failure alarm triggered for node associated with Ticket ${ticketId}!`, 'error');
        addTerminalLog(`[WARN] CPU usage spiked to 97% on telemetry tracker.`, 'warn');
        addTerminalLog(`[ERROR] Daemon: Connection reset by peer on target socket sshd.`, 'error');

        alert(`Critical alarm triggered for Ticket ${ticketId}. Server resource allocation spiked to maximum! Check live charts.`);
    }

    // ==========================================
    // GENERATOR ACTIONS
    // ==========================================
    const presets = [
        { priority: "High", category: "Service", title: "SSH service down on practice server" },
        { priority: "High", category: "Web", title: "Apache web service not responding" },
        { priority: "Medium", category: "Firewall", title: "Firewall blocks web application port" },
        { priority: "High", category: "Storage", title: "Disk usage alert generated" },
        { priority: "Medium", category: "Permission", title: "Wrong permission on shared directory" },
        { priority: "Medium", category: "User Management", title: "User account locked" },
        { priority: "Low", category: "Service", title: "Cron service stopped" },
        { priority: "High", category: "SELinux", title: "SELinux context issue on web file" },
        { priority: "High", category: "Network", title: "NetworkManager service inactive" },
        { priority: "Medium", category: "Security", title: "Failed login report investigation" },
        { priority: "Medium", category: "Permission", title: "Wrong owner on application directory" },
        { priority: "Low", category: "Package", title: "Package missing: tar" }
    ];

    const btnGenerate = document.getElementById('btn-generate-tickets');
    if (btnGenerate) {
        btnGenerate.addEventListener('click', () => {
            const countInput = document.getElementById('generate-count');
            const count = countInput ? parseInt(countInput.value) || 1 : 10;
            
            const tickets = getTickets();
            
            for (let i = 0; i < count; i++) {
                const randomPreset = presets[Math.floor(Math.random() * presets.length)];
                const randomId = "#" + Math.floor(1000 + Math.random() * 9000);
                const randomOperator = "operator0" + (1 + Math.floor(Math.random() * 3));
                
                tickets.push({
                    id: randomId,
                    priority: randomPreset.priority,
                    category: randomPreset.category,
                    title: randomPreset.title,
                    status: "open",
                    assigned: randomOperator,
                    score: 0
                });
            }

            saveTickets(tickets);
            updateMetrics();
            renderTicketsTable();
            addTerminalLog(`[INFO] Generated ${count} mock operational incidents into queue.`, 'info');
        });
    }

    const btnReset = document.getElementById('btn-reset-lab');
    if (btnReset) {
        btnReset.addEventListener('click', () => {
            localStorage.removeItem('cqx_tickets');
            updateMetrics();
            renderTicketsTable();
            addTerminalLog(`[INFO] Active console reset. Queue flushed successfully.`, 'info');
            alert("Incidents board reset.");
        });
    }

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
