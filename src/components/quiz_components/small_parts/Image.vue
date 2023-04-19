<template>
    <div class="image-container" v-if="imageUrl">
        <img class="image" v-bind:src="imageUrl" />
    </div>
</template>

<script>
export default {
    props: [
        'imageUrl',
    ],
    data(){
        return {

        }
    },
    mounted() {
       
    },
    computed:{
        
    },
    methods:{
       
    }

}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.image-container {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 0.5rem;
    .image {
        width: 40%;
    }
}

</style>