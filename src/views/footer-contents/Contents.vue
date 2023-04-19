<template>
    <div class='contents-wrapper'>
        <div class="main-wrapper">
            <div class="title-white">{{ param[0].toUpperCase()}}{{ param.slice(1) }}</div>
        <Quiz
        v-if="param==='quiz'"
        />
        <Community
        v-if="param==='community'"/>
    </div>
    </div>
</template>

<script>
import Quiz from "@/components/abouts/Quiz.vue";
import Community from "@/components/abouts/Community.vue";

export default {
    components: {
        Quiz,
        Community
    },
    data() {
        return {
        }
    },
    // beforeMount() {
    //     console.log("BM")
    //     this.$store.commit('setIsLoading', false)
    // },
    computed:{
        param() {
            this.$store.commit('setIsLoading', false)
            return this.$route.params.key
        }
    },

}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";
.title-white {
    margin: 1rem 0;
}
.contents-wrapper{
    display: flex;
    justify-content: center;
}
.main-wrapper{
    width: 800px;
}

</style>