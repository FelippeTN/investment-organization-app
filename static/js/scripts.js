document.addEventListener('DOMContentLoaded', function () {
    const portfolioCanvas = document.getElementById('portfolioChart');
    if (portfolioCanvas) {
        try {
            const loadingSpinner = portfolioCanvas.parentElement.querySelector('.chart-loading');
            if (loadingSpinner) loadingSpinner.classList.remove('hidden'); // Show spinner
            portfolioCanvas.classList.add('opacity-50'); // Add loading state
            const operations = JSON.parse(portfolioCanvas.dataset.operations || '[]');

            const portfolio = {};
            operations.forEach(op => {
                const ticker = op.ticker;
                const quantity = parseFloat(op.quantity);
                const unitaryPrice = parseFloat(op.unitary_price.toString().replace(',', '.'));
                const type = op.type.toLowerCase();

                if (!portfolio[ticker]) {
                    portfolio[ticker] = { quantity: 0, totalValue: 0, totalCost: 0 };
                }

                if (type === 'compra') {
                    portfolio[ticker].quantity += quantity;
                    portfolio[ticker].totalCost += quantity * unitaryPrice;
                } else if (type === 'venda') {
                    portfolio[ticker].quantity -= quantity;
                    portfolio[ticker].totalCost -= quantity * unitaryPrice;
                }

                if (portfolio[ticker].quantity > 0) {
                    portfolio[ticker].totalValue = portfolio[ticker].quantity * (portfolio[ticker].totalCost / portfolio[ticker].quantity);
                } else {
                    portfolio[ticker].totalValue = 0;
                }
            });

            const labels = [];
            const values = [];
            for (const ticker in portfolio) {
                if (portfolio[ticker].quantity > 0 && portfolio[ticker].totalValue > 0) {
                    labels.push(ticker);
                    values.push(portfolio[ticker].totalValue);
                }
            }

            if (labels.length > 0 && values.length > 0) {
                const ctx = portfolioCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: values,
                            backgroundColor: [
                                '#1E3A8A', // Deep Navy
                                '#3B82F6', // Bright Blue
                                '#10B981', // Emerald Green
                                '#F59E0B', // Amber
                                '#EF4444', // Red
                                '#8B5CF6', // Purple
                            ],
                            borderColor: '#FFFFFF',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    color: '#1F2937',
                                    font: {
                                        size: 14,
                                        weight: '500'
                                    }
                                }
                            },
                            tooltip: {
                                backgroundColor: '#111827',
                                titleColor: '#FFFFFF',
                                bodyColor: '#D1D5DB',
                                callbacks: {
                                    label: function (context) {
                                        let label = context.label || '';
                                        let value = context.raw || 0;
                                        return `${label}: R$ ${value.toFixed(2)}`;
                                    }
                                }
                            }
                        }
                    }
                });
                portfolioCanvas.classList.remove('opacity-50'); // Remove loading state
                if (loadingSpinner) loadingSpinner.classList.add('hidden'); // Hide spinner
            }
        } catch (error) {
            console.error('Erro ao renderizar o gráfico de portfólio:', error);
            portfolioCanvas.classList.remove('opacity-50');
            if (loadingSpinner) loadingSpinner.classList.add('hidden');
        }
    }

    const sectorCanvas = document.getElementById('sectorChart');
    if (sectorCanvas) {
        try {
            const loadingSpinner = sectorCanvas.parentElement.querySelector('.chart-loading');
            if (loadingSpinner) loadingSpinner.classList.remove('hidden'); // Show spinner
            sectorCanvas.classList.add('opacity-50'); // Add loading state
            const sectors = JSON.parse(sectorCanvas.dataset.sectors || '{}');

            const labels = [];
            const values = [];
            for (const sector in sectors) {
                if (sectors[sector] > 0) {
                    labels.push(sector);
                    values.push(sectors[sector]);
                }
            }

            if (labels.length > 0 && values.length > 0) {
                const ctx = sectorCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: values,
                            backgroundColor: [
                                '#1E3A8A',
                                '#3B82F6',
                                '#10B981',
                                '#F59E0B',
                                '#EF4444',
                                '#8B5CF6',
                            ],
                            borderColor: '#FFFFFF',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    color: '#1F2937',
                                    font: {
                                        size: 14,
                                        weight: '500'
                                    }
                                }
                            },
                            tooltip: {
                                backgroundColor: '#111827',
                                titleColor: '#FFFFFF',
                                bodyColor: '#D1D5DB',
                                callbacks: {
                                    label: function (context) {
                                        let label = context.label || '';
                                        let value = context.raw || 0;
                                        return `${label}: R$ ${value.toFixed(2)}`;
                                    }
                                }
                            }
                        }
                    }
                });
                sectorCanvas.classList.remove('opacity-50'); // Remove loading state
                if (loadingSpinner) loadingSpinner.classList.add('hidden'); // Hide spinner
            }
        } catch (error) {
            console.error('Erro ao renderizar o gráfico de setores:', error);
            sectorCanvas.classList.remove('opacity-50');
            if (loadingSpinner) loadingSpinner.classList.add('hidden');
        }
    }
});