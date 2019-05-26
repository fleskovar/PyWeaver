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
                <v-card style='overflow-y: scroll' height='300px'>
                    <v-treeview :items="libraryTree" ref='tree'>
                        <template v-slot:prepend="{ item }">
                        <v-icon v-if="item.children">folder</v-icon>
                        <v-icon v-if="!item.children">insert_drive_file</v-icon>
                        </template>

                        <template v-slot:label="{item}">
                            {{item.name}}
                        </template>

                    </v-treeview>
                </v-card>
            </v-card-text>

		</v-card>
    </v-dialog>
</template>

<script>
export default {
    data(){
        return{
        }
    },
    methods:{
        closeDialog(){
            this.$store.commit('set_dialog_open', false);
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
