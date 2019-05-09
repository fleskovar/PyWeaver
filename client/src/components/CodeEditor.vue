<template>
	<codemirror id='code_editor' :options='editorOptions' v-model="code"/>
</template>

<script>

export default{
	data(){
		return{
			code: '',
			editorOptions: {
				mode: 'python',
				theme: 'default	',
				lineNumbers: true,
				indentUnit: 4,
				indentWithTabs: true,
				smartIndent: true,				
			}
		}
	}
}


</script>

<style>
</style>