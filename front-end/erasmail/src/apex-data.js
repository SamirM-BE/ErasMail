const radialBarPotentialImpact = {
    chart: {
        type: "radialBar",
    },
    series: [],
    colors: ["hsl(141, 71%, 48%)"],
    plotOptions: {
        radialBar: {
            track: {
                background: "hsl(48, 100%, 67%)",
                opacity: 0.4,
            },
            dataLabels: {
                name: {
                    fontSize: "22px",
                    color: ["hsl(217, 71%, 53%)"]
                },
                value: {
                    fontSize: "16px",
                    formatter: function (val) {
                        return val + '% saved'
                    }
                },
                total: {
                    show: true,
                    label: "Currently saved",
                    formatter: function (w) {
                        return (
                            (
                                w.globals.seriesTotals.reduce((a, b) => {
                                    return a + b;
                                }, 0) / w.globals.series.length
                            ).toPrecision(2) + "% / Total potential"
                        );
                    },
                },
            },
        },
    },
    labels: [],
}

const lineSizeMailbox = {
    chartOptions: {
        chart: {
            id: "vuechart-example",
            toolbar: {
                show: false,
            },
        },
        title: {
            text: 'Total saved co2',
            align: 'left'
        },
        xaxis: {
            categories: ["Before ErasMail", "13/03/2021", "Today"],
        },
    },
    series: [
        {
            name: "CO2 grams",
            data: [0, 632, 951],
        },
    ]
}

export { radialBarPotentialImpact, lineSizeMailbox }