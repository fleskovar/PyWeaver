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
                <v-container grid-list-md>
                    <v-layout row wrap>
                        <v-flex xs6>
                            <v-card style='overflow-y: scroll; border: 2px solid grey; border-radius: 1px;' height='500px' flat>
                                <v-treeview :items="libraryTree" ref='tree' activatable :active.sync="selected_folder" return-object>                        
                                        <template v-slot:prepend="{ item }">
                                            <div @click="hover_tree_id = item.id">
                                                <v-icon v-if="item.children">folder</v-icon>
                                                <v-icon v-if="!item.children">insert_drive_file</v-icon>
                                            </div>
                                        </template>

                                        <template v-slot:label="{item}">
                                            <div @click="hover_tree_id = item.id">
                                                <v-text-field v-if= 'false' :value='item.name' disabled solo flat single-line/>
                                                <span>{{item.name}}</span>
                                                &ensp;
                                                <a><v-icon v-if="item.id == hover_tree_id" @click='openEditNameDialog(item)'>edit</v-icon></a>
                                                <a><v-icon v-if="item.id == hover_tree_id && item.children" @click='openNewFolderDialog(item)'>create_new_folder</v-icon></a>
                                                <a><v-icon v-if="item.id == hover_tree_id" @click='openDeleteFolderDialog(item)'>delete_forever</v-icon></a>                                    
                                            </div>
                                        </template>                        
                                </v-treeview>
                            </v-card>
                        </v-flex>
                        
                        <v-flex xs6 >
                            <v-card flat height='500px'>
                                <v-text-field label="Node Template Name" v-model='save_name' :rules="[rules.required]" clearable/>
                                
                                <v-textarea
                                label="Node Description"
                                v-model="description"
                                no-resize
                                outline
                                ></v-textarea>

                                <v-textarea
                                label="Search keywords"
                                v-model="keywords"
                                hint = 'Comma separated keywords'
                                no-resize
                                outline
                                persistent-hint
                                ></v-textarea>
                            </v-card>
                        </v-flex>
                    
                    </v-layout>
                </v-container>
                    
            </v-card-text>

            <v-card-actions>     
				<v-spacer/>         
				<v-btn color="blue" flat dark @click='saveNode'>Save</v-btn>                          
			</v-card-actions>

		</v-card>


        <v-dialog v-model='add_folder_dialog' width='500px'>
            <v-card>      
                <v-toolbar dark color="gray">              
                    <v-toolbar-title>New Folder</v-toolbar-title>   
                    <v-spacer></v-spacer>
                    <v-toolbar-items>                
                    <v-btn icon dark @click="add_folder_dialog = false">
                        <v-icon>close</v-icon>
                    </v-btn>
                    </v-toolbar-items>
                </v-toolbar>

                <v-card-text>
                    <v-text-field label="New Folder Name" v-model='new_folder_name' :rules="[rules.required]"/>
                </v-card-text>

                <v-card-actions>   
                    <v-btn color="green" flat dark @click='createNewFolder'>Create</v-btn>    
                    <v-spacer/>         
                    <v-btn color="red" flat dark @click="add_folder_dialog = false">Cancel</v-btn>                          
                </v-card-actions>
		    </v-card>
        </v-dialog>

        <v-dialog v-model='delete_folder_dialog' width='500px'>
            <v-card>      
                <v-toolbar dark color="gray">              
                    <v-toolbar-title>Delete Folder?</v-toolbar-title>   
                    <v-spacer></v-spacer>
                    <v-toolbar-items>                
                    <v-btn icon dark @click="delete_folder_dialog = false">
                        <v-icon>close</v-icon>
                    </v-btn>
                    </v-toolbar-items>
                </v-toolbar>

                <v-card-text>
                    Are you sure you want to permanently delete the folder and all the content inside?
                </v-card-text>

                <v-card-actions>   
                    <v-btn color="blue" flat dark @click='deleteFolder'>Yes, Delete It</v-btn>    
                    <v-spacer/>         
                    <v-btn color="blue" flat dark @click="delete_folder_dialog = false">No</v-btn>                          
                </v-card-actions>
		    </v-card>
        </v-dialog>

        <v-dialog v-model='edit_name_dialog' width='500px'>
            <v-card>      
                <v-toolbar dark color="gray">              
                    <v-toolbar-title>Edit Name</v-toolbar-title>   
                    <v-spacer></v-spacer>
                    <v-toolbar-items>                
                    <v-btn icon dark @click="edit_name_dialog = false">
                        <v-icon>close</v-icon>
                    </v-btn>
                    </v-toolbar-items>
                </v-toolbar>

                <v-card-text>
                    <v-text-field label="New Name" v-model='new_item_name' :rules="[rules.required]"/>
                </v-card-text>

                <v-card-actions>   
                    <v-btn color="green" flat dark @click='renameItem'>Rename</v-btn>    
                    <v-spacer/>         
                    <v-btn color="red" flat dark @click="edit_name_dialog = false">Cancel</v-btn>                          
                </v-card-actions>
		    </v-card>
        </v-dialog>


    </v-dialog>
</template>

<script>
export default {
    data(){
        return{
            selected_folder: [],
            rename_dialog: false,
            name_dialog: false,
            save_name: 'New Template',
            rules:{
                required: value => !!value || 'Required.',
            },
            hover_tree_id: -1,    
            add_folder_dialog: false,
            delete_folder_dialog: false,
            edit_name_dialog: false,
            selected_item: {},    
            new_folder_name: 'New Folder',  
            new_item_name: '',
            description: 'Short description of what the node does.',
            keywords: '',
        }
    },
    methods:{
        closeDialog(){
            this.description = 'Short description of what the node does.';
            this.$store.commit('set_dialog_open', false);
        },
        saveNode(){
            
            if(this.save_name)
            {
                var data = {};
                data.overwrite = false;
                var proceed = true;
                if(this.selected_folder[0].lib_id){
                    proceed = confirm("Overwrite existing module?");
                    data.overwrite = true;
                }
                
                if(proceed){                                    

                    let node = this.$store.state.selected_node;
                    
                    var node_data = {};
                    node_data.name = this.save_name;
                    node_data.code = node.code;
                    node_data.display_code = node.display_code;
                    node_data.display_act_code = node.display_act_code;
                    
                    var meta_obj = {
                        description: this.description,
                        keywords: this.keywords,
                        test_vals: '',
                        connections: ''
                    };
                    node_data.meta = JSON.stringify(meta_obj);

                    var path = this.selected_folder[0].path;

                    data.path = path;
                    data.node_data = node_data;

                    this.$socket.emit('save_to_library', data);
                    this.closeDialog();
                }
            }
        },        
        openNewFolderDialog(item){
            this.selected_item = item;
            this.new_folder_name = 'New Folder';
            this.add_folder_dialog = true;
        },
        openDeleteFolderDialog(item){
            this.selected_item = item;
            this.delete_folder_dialog = true;
        },
        openEditNameDialog(item){
            this.selected_item = item;
            this.new_item_name = item.name;
            this.edit_name_dialog = true;
        },
        createNewFolder(){
            var folder_data = {
                path: this.selected_item.path,
                name: this.new_folder_name
            };
            this.$socket.emit('new_folder', folder_data);
            this.add_folder_dialog = false;
        },
        deleteFolder(){
            var path = this.selected_item.path;
            this.$socket.emit('delete_folder', path);
            this.delete_folder_dialog = false;
        },
        renameItem(){
            var folder_data = {
                path: this.selected_item.path,
                name: this.new_item_name
            };
            this.$socket.emit('rename_folder', folder_data);
            this.edit_name_dialog = false;
        },
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
