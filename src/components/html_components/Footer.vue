<template>
    <footer class="footer-wrapper">
        <router-link class="img" to="/" >
            <img src="@/assets/logo.png">
        </router-link>
        <div class="footer-container">
            <div class="footer-contents"
            v-for="(contents,keyContent,index) in footerContents"
            v-bind:key="index">
                <div class="content-box">
                    <div class="content-title" >
                        {{keyContent}}
                    </div>
                    <div class="content-loop"
                    v-for="(path,key,contentIndex) in contents"
                    v-bind:key="contentIndex">
                        <p @click="routeSorting(path,keyContent)">{{ key }}</p>
                    </div>
                </div>                
            </div>
        </div>
        <div class="social-link">
            <div class="space">
            </div>
            <img @click="twitter" class="social-img" src="@/assets/twitter.png">
        </div>
        <p class="copy-right">Copyright (c) 2022</p>
    </footer>
</template>

<script>
import {router} from "/src/main.js"

export default {
    
    data(){
        return{
            tweetUrl:'',
            footerContents:{
                //name and path pare
                'ガイドとヘルプ':{
                    'About':'about',
                    '利用規約':'terms-and-conditions',
                    '個人情報の取り扱い':'privacy',
                    '問い合わせ':'enquire',
                    'FAQ':'faq'
                },
                'コンテンツ':{
                    'Quiz':'contents/quiz',
                    'Community':'contents/community'
                },
                // '運営':{
                //     '運営会社':''
                // }
            },
        }
    },
    methods:{
        twitter(){
            const domain = window.location.href
            var url = "http://google.com";
            const shareURL = 
            'https://twitter.com/intent/tweet?text=' + "日本語学習ならNEKO-Japanese！"
            + "%0A" +encodeURIComponent(domain)
            + "%0A" + "%0A" + "%20%23" + "NEKOJapnese"
            + "%0A" + "%20%23" + "日本語学習" 
            + "%0A" + "%20%23" + "日本語学習プラットフォーム"
            window.open(shareURL)
        },
        routeSorting(pathArg) {
            const path =  '/' + pathArg
            router.push(path)
        }
    },
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.footer-wrapper{
    background-color: transparent;
    background-image: none;
    border-top: solid $dark-blue;
    position: relative;
    .img{
        position: absolute;
        flex-basis: 50%;
        display: flex;
        img{
            width: 5rem;
            height: 5rem;
            margin-left: 1rem;
        }
    }
    .footer-container{
        display: flex;
        justify-content: flex-end;
        margin-right: 2rem;
        .footer-contents{
            display: flex;
            justify-content: flex-end;
            .content-box{
                margin-top: 1rem;
                margin-right: 0.5rem;
                margin-left: 0.5rem;
                .content-title{
                    color: $base-white;
                    font-weight: bold;
                    font-size: 1.2rem;
                    border-bottom: solid gray;
                }
                .content-loop{
                        color: $base-white;
                        // margin-top: 0.5rem;
                        transition: .3s;
                        padding: 0.2rem 0.2rem;
                }
                .content-loop:hover {
                    background: rgba($color: $back-white, $alpha: 0.1)
                }
             }
         }
    }
    .copy-right{
        color: $base-white;
        padding: 1rem;
        
    }
    .social-link{
        .social-img{
            width: 3rem;
            transition: .5s;
        }
        .social-img:hover{
            box-shadow: 0.5px 0.5px 10px 2.5px #cbfaed;
            border-radius: 7px;
        }
    }
}
@media(max-width: 480px){
    .footer-wrapper{
        .img{
            position: absolute;
            flex-basis: 50%;
            display: flex;
            img{
                width: 5rem;
                height: 5rem;
                margin-left: 1rem;
            }
        }
        .footer-container{
            display: flex;
            justify-content: center;
            flex-direction: column;
            width: 100%;
            .footer-contents{
                display: flex;
                justify-content: center;
                .content-box{
                    margin-top: 1rem;
                    margin-bottom: 1rem;
                    .content-title{
                        color: $base-white;
                        font-weight: bold;
                        font-size: 1.2rem;
                        border-bottom: solid gray;
                    }
                    .content-loop{
                            color: $base-white;
                            margin-top: 0.5rem;
                        }
                }
            }
        }
        .copy-right{
            color: $base-white;
            margin-top: 1rem;
            padding: 4rem;
            
        }
    }
}
</style>