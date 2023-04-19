<template>
    <div class="note-detail-wrapper">
        <div class="main-wrapper">
            <div class="title-white">
                運営からのお知らせ
            </div>
            <div class="content-wrapper">
                <div class="detail-header">
                    <div class="detail-type">{{ noteDetail.type }} </div>
                    <DateToLocal
                    :UTCDate='noteDetail.issued_date'/>
                </div>
                <div class="img-container" v-if="noteDetail.image">
                    <img :src="noteDetail.image">
                </div>
                <div class="detail-title">{{ noteDetail.title }}</div>
                <div class="detail-body">{{ noteDetail.body }}</div>
                <div class="back-list" @click='goToNoteList'>
                    <div class="back-text">{{ backText }}</div>
                </div>
            </div>
        </div>
    </div>
  
</template>

<script>
import DateToLocal from "@/components/parts/DateToLocal.vue";
import {router} from "../main.js"
export default {
    components: {
        DateToLocal
    },
    data(){
        return{
            backText:'<<一覧へ戻る'
        }
    },
    created(){
        this.$store.dispatch('getNotificationDetail',this.$route.params.slug)
        this.$store.commit('setIsLoading', false)
    },
    mounted(){
    },
    computed:{
        noteDetail(){
            return this.$store.getters.notificationDetail

        },
    },
    methods: {
        goToNoteList() {
            router.push(`/note-list/`)
        },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";

.note-detail-wrapper {
        display: flex;
        justify-content: center;
        color: white;
    }
    .title-white{
        margin: 2rem 0;
    }
    .detail-header{
        display: flex;
        align-items: center;
        .detail-type {
            border: solid $dull-red;
            color: $dull-red;
            // margin:0 2rem ;
            margin-right: 1rem;
            padding: 0 0.3rem;
        }
    }
    .img-container{
        margin-top: 2rem;
    }
    .detail-title {
        font-size: 1.5rem;
        margin: 3rem 0;
        font-weight: bold;
    }
    .detail-body {
        white-space: pre-wrap;
    }
    .back-list {
        display: flex;
        margin-top: 5rem;
        .back-text {
            // margin-left: 2rem;
            color: $lite-green;
            transition: .3s;
        }
        .back-text:hover {
            color: $lite-green-hover;
        }
    }
.content-wrapper{
    padding: 1rem;
    background: rgba($color: $back-white, $alpha: 0.1)
}


</style>