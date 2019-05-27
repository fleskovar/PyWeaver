<template>
    <v-dialog v-model="save_dialog" width="800" persistent>          
		<v-card>      
			<v-toolbar dark color="gray">              
				<v-toolbar-title>Save to Library</v-toolbar-title>   
				<v-spacer></v-spacer>
				<v-toolbar-items>                
				<v-btn icon dark @click="closeDialog">
					<v-icon>close</v-icon>
				</v-btn>
				</v-toolbar-items>
			</v-toolbar>

            <v-card-text>
                <v-text-field label="Node" v-model='save_name' :rules="[rules.required]"/>

                <v-card style='overflow-y: scroll' height='300px' flat>
                    <v-treeview :items="libraryTree" ref='tree' activatable :active.sync="selected_folder" return-object>
                        <template v-slot:prepend="{ item }">
                        <v-icon v-if="item.children">folder</v-icon>
                        <v-icon v-if="!item.children">insert_drive_file</v-icon>
                        </template>

                        <template v-slot:label="{item}">
                            <v-text-field v-if= 'false' :value='item.name' disabled solo flat single-line/>
                            <span>{{item.name}}</span>
                        </template>

                    </v-treeview>
                </v-card>

            </v-card-text>

            <v-card-actions>     
				<v-spacer/>         
				<v-btn color="blue" flat dark @click='saveNode'>Save</v-btn>                          
			</v-card-actions>

		</v-card>
    </v-dialog>
</template>

<script>
export default {
    data(){
        return{
            selected_folder: [],
            rename_dialog: false,
            name_dialog: false,
            save_name: '',
            rules:{
                required: value => !!value || 'Required.',
            }
        }
    },
    methods:{
        closeDialog(){
            this.$store.commit('set_dialog_open', false);
        },
        saveNode(){
            if(this.save_name)
            {
                var data = {};
                var node_data = {};

                let node = this.$store.state.selected_node;
                node_data.name = this.save_name;
                node_data.code = node.code;
                node_data.display_code = node.display_code;
                node_data.display_act_code = node.display_act_code;

                var path = this.selected_folder[0].path;

                data.path = path;
                data.node_data = node_data;

                this.$socket.emit('save_to_library', data);
                this.closeDialog();
            }
        }
    },
    computed:{
        save_dialog:{
            get(){ return this.$store.state.save_dialog}            
        },
        libraryTree:{
            get(){
                return this.$store.state.libraryTree;
            }
        }
    }
}
</script>

<style>

</style>
