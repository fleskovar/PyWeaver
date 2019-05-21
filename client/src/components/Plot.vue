<template>
	<div>
		<div :ref="chart.uuid"></div>   
	</div>
</template>

<script>
import Plotly from 'plotly.js-dist';
export default {
    props: ["chart"],
    mounted() {
        Plotly.plot(this.$refs[this.chart.uuid], this.chart.traces, this.chart.layout);
    },
    watch: {
        chart: {
        handler: function() {
            console.log('changed');
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
