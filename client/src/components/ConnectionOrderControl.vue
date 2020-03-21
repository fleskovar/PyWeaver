<template>
    <div>
        <v-data-table dense hide-actions :headers="headers" :items="vars_list">
            <template v-slot:items="props">   
                <td class="text-xs-left">{{ props.item.node_id }}</td>
                <td class="text-xs-left">{{ props.item.var_name }}</td>
                <td class="text-xs-left">{{ props.item.var_type }}</td>
                <td>
                    <v-item-group dense>
                        <v-btn flat small icon><v-icon size="15">keyboard_arrow_up</v-icon></v-btn>
                        <v-btn flat small icon><v-icon size="15">keyboard_arrow_down</v-icon></v-btn>
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
                { text: 'Node ID', value: 'node_id' },
                { text: 'Variable', value: 'var_name' },
                { text: 'Type', value: 'var_type' },
                { text: 'Order', value: 'order' },
            ],
            
    }),
    methods:{
        
    },
    computed:{
        vars_list: 
        {
            get: function()
            {
                return this.$store.state.connection_inspector_connections;
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