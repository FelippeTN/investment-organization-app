document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('portfolioChart');
    if (canvas) {
        try {
            const operations = JSON.parse(canvas.dataset.operations || '[]');

            // Calcular composição da carteira
            const portfolio = {};
            operations.forEach(op => {
                const ticker = op.ticker;
                const quantity = parseFloat(op.quantity);
                const unitaryPrice = parseFloat(op.unitary_price.toString().replace(',', '.'));
                const type = op.type.toLowerCase();

                if (!portfolio[ticker]) {
                    portfolio[ticker] = { quantity: 0, totalValue: 0, totalCost: 0 };
                }

                // Ajustar quantidade (compra aumenta, venda diminui)
                if (type === 'compra') {
                    portfolio[ticker].quantity += quantity;
                    portfolio[ticker].totalCost += quantity * unitaryPrice;
                } else if (type === 'venda') {
                    portfolio[ticker].quantity -= quantity;
                    portfolio[ticker].totalCost -= quantity * unitaryPrice;
                }

                // Calcular preço médio (se houver quantidade)
                if (portfolio[ticker].quantity > 0) {
                    portfolio[ticker].totalValue = portfolio[ticker].quantity * (portfolio[ticker].totalCost / portfolio[ticker].quantity);
                } else {
                    portfolio[ticker].totalValue = 0;
                }
            });

            // Preparar dados para o gráfico
            const labels = [];
            const values = [];
            for (const ticker in portfolio) {
                if (portfolio[ticker].quantity > 0 && portfolio[ticker].totalValue > 0) {
                    labels.push(ticker);
                    values.push(portfolio[ticker].totalValue);
                }
            }

            if (labels.length > 0 && values.length > 0) {
                const ctx = canvas.getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: values,
                            backgroundColor: [
                                '#10B981', 
                                '#3B82F6', 
                                '#EF4444', 
                                '#F59E0B',
                                '#8B5CF6', 
                                '#EC4899', 
                            ],
                            borderColor: '#1F2937', 
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
                                    color: '#D1D5DB' // gray-300
                                }
                            },
                            tooltip: {
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
            }
        } catch (error) {
            console.error('Erro ao renderizar o gráfico:', error);
        }
    }
});