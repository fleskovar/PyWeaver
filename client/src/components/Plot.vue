<template>
	<div>
		<div ref="plot_div"></div>   
	</div>
</template>

<script>
import Plotly from 'plotly.js-dist';
export default {
    props: ["chart"],
    mounted() {
        Plotly.plot(this.$refs.plot_div, this.chart.traces, this.chart.layout, {displayModeBar: false});
    },
    watch: {
        chart: {
        handler: function() {
            Plotly.newPlot(
            this.$refs[this.chart.uuid],
            this.chart.traces,
            this.chart.layout
            );
        },
        deep: true
        }
    }
}
</script>
