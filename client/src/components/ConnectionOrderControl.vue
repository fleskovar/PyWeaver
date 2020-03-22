<template>
    <div>
        <v-data-table dense hide-actions :headers="headers" :items="vars_list">
            <template v-slot:items="props">   
                <td class="text-xs-left">{{ props.index }}</td>
                <td class="text-xs-left">{{ props.item.node_id }}</td>
                <td class="text-xs-left">{{ props.item.var_name }}</td>
                <td class="text-xs-left">{{ props.item.var_type }}</td>
                <td>
                    <v-item-group dense>
                        <v-btn flat small icon @click='move_conn(props, 1)'><v-icon size="15">keyboard_arrow_up</v-icon></v-btn>
                        <v-btn flat small icon @click='move_conn(props, -1)'><v-icon size="15">keyboard_arrow_down</v-icon></v-btn>
                    </v-item-group>
                </td>
            </template>   
        </v-data-table>
        
    </div>
</template>

<script>
export default {
    data: () => ({
            
            headers: [
                { text: '#', value: 'index' },      
                { text: 'Node ID', value: 'node_id' },
                { text: 'Variable', value: 'var_name' },
                { text: 'Type', value: 'var_type' },
                { text: 'Order', value: 'order' },
            ],
            
    }),
    methods:{
        move_conn: function(props, dir){
            var sort_data = {};
            sort_data.position = props.index;
            sort_data.direction = dir;
            sort_data.node_id = this.$store.state.connection_inspector_id.node_id;
            sort_data.var_name = this.$store.state.connection_inspector_id.var_name;

            var new_pos = props.index - dir;
            var max_index = this.vars_list.length-1;

            if(new_pos > -1 && new_pos < max_index){
                this.$store.dispatch('sort_connection', sort_data);
            }
        }        
    },
    computed:{
        vars_list: 
        {
            get: function()
            {
                return this.$store.state.connection_inspector_connections;
            }
        },

        var_name:
        {
            get: function(){
                return this.$store.state.connection_inspector_id;
            }
        }
    }
}
</script>

<style>
tbody tr:nth-of-type(even) {
    background-color: rgba(65, 65, 65);
  }

  tbody tr:nth-of-type(odd) {
    background-color: rgb(88, 88, 88);
  }

</style>