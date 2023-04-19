<template>
    <div class="note-list-wrapper" >
        <div class="main-wrapper">
            <div class="title-white">
                運営からのお知らせ
            </div>
            <div class="paragraph-container-note">
                <div class="note-wrapper">
                    <div class="note-container" v-for="(note, index) in noticeFromTeam"
                        :key="index">
                        <div class="note-header">
                            <div class="note-type">{{ note.type }}</div>
                            <DateToLocal
                            :UTCDate='note.issued_date'/>
                        </div>
                        <div class="note-title">{{ note.title.substr(0,17) }}</div>
                        <div class="note-body">{{ note.body.substr(0,20)+'...' }}</div>
                        <div class="note-next-container">
                            <div class="note-next" @click='goToNoteDetail(note.slug)'>
                                続きを見る>>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  
</template>

<script>
import DateToLocal from "@/components/parts/DateToLocal.vue";
import { router } from "../main.js"
export default {
    components: {
        DateToLocal
    },
    created() {
        this.$store.commit('setIsLoading', false)
        if(!this.$store.getters.getNotificationList) {
            this.$store.dispatch('getNotificationList')
        }
    },
    beforeMount() {
        this.$store.commit('setIsLoading', false)
    },
    computed:{
        noticeFromTeam(){
            return this.$store.getters.getNotificationList
        }

    },
    methods: {
        goToNoteDetail(slug) {
            router.push(`/note-detail/${slug}`)
        },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
    .note-list-wrapper {
        display: flex;
        justify-content: center;
    }
    .title-white{
        margin: 2rem 0;
    }
    .note-wrapper {
        width: 100%;
        display: flex;
        flex-direction: column;
        // .note-container:hover{
        //     background: $base-white; 
        // }
        // .note-container:hover .note-body{
        //     color: $dark-blue; 
        // }
        // .note-container:hover .note-date{
        //     color: $dark-blue; 
        // }
        .note-container {
            transition: .3s;
            display: flex;
            flex-direction: column;
            min-height: 130px;
            justify-content: space-between;
            background: white;
            border: solid $dark-blue;
            margin-bottom: 0.3rem;
            .note-header{
                display: flex;
                padding: 0.5rem;
                // justify-content: center;
                align-items: center;
                .note-type {
                    min-width: 7rem;
                    border: solid $dull-red;
                    font-weight: bold;
                    padding: 0 0.5rem;
                    margin-right: 0.5rem;
                    color: $dull-red;
                }
                .note-date{
                    transition: .3s;
                }
            }
            .note-title {
                font-weight: bold;
                font-size:1.3rem;
                text-decoration: underline;
                color: darkgray;
            }
            .note-body {
                margin-bottom: 0.4rem;
                transition: .3s;
            }
            .note-next-container {
                width: auto;
                text-align: right;
                .note-next {
                    text-align: right;
                    display: inline-block;
                    margin-right: 1rem;
                    margin-top: 1rem;
                    margin-bottom: 0.5rem;
                    color: $dark-blue;
                    transition: .3s;
                }
                .note-next:hover {
                    color: $lite-blue;
                }
            }
        }
    }


</style>