<template>
    <div class="all-cover-wrapper">
        <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
            <div class="lds-dual-ring"></div>
        </div>
        <div class="main-wrapper">
            <h1 class='title-white'>質問板</h1>
            <div class="related-title">検索結果</div>
            <div class="question-wrapper">
                <div
                v-for="(question,questionindex) in searchedQuestion"
                v-bind:key="questionindex">
                    <div class='question-list' @click="getDetail(question.slug)">
                        <div 
                         class="tag-wrapper">
                            <div 
                             class="tag"
                             v-for="(tag,tagindex) in question.tag" 
                             v-bind:key="tagindex">{{ tag.tag }}</div>
                        </div>
                        <div class="question-title">{{ question.title }}</div>
                        <div class="question-description">{{ question.description.substr(0,10)+'...' }}</div>
                        <div class='good-like-wrapper'>
                            <i class="far fa-heart"></i>
                            <div class="good" v-if="question.liked_num[0]">{{ question.liked_num[0].liked_num }}</div>
                            <div class="date">作成日：{{ question.created_on }}</div>
                        </div>
                    </div>        
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {router} from "/src/main.js"
export default {
    data(){
        return{
        }
    },
    props:[
        'searchedQuestion',
    ],
    mounted(){
    },
    methods: {
        getDetail(slug){
            router.push(`/board-detail/${slug}` )
        },   
    }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";

.main-wrapper{
        display: flex;
        flex-direction: column;
        align-items: center;
        .related-title{
            margin-top: 2rem;
            color: $dark-blue;
        }
        .question-wrapper{
            margin: 1rem;
            width: 85%;
            .question-list{
                border: solid $base-color;
                margin-bottom: 0.5rem;
                width:100%;
                background: rgb(252, 252, 252);
                display: flex;
                flex-direction: column;
                .tag-wrapper{
                    display: flex;
                    width: 100%;
                    .tag{
                        border: solid black;
                        border-radius: 50vh;
                        background: rgb(230, 230, 230);
                        margin-top: 0.5rem;
                        margin-left: 0.3rem;
                        margin-bottom: 0.5rem;
                        padding: 0.5rem;
                        min-width: 3rem;
                    }
                }
                .good-like-wrapper{
                    display: flex;
                    .fa-heart{
                        color: rgb(221, 36, 221);
                        margin-left: 0.5rem;
                        margin-right: 0.3rem;
                        margin-top: 0.2rem;
                    }
                    .date{
                        margin-left: 0.5rem;
                    }
                }
            }
        }
    }
</style>