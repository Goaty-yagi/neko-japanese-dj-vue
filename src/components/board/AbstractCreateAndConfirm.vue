<template>
    <div class="l-wrapper">
        <div class='l-container'>
            <div class="title-blue">
                 <p>{{ obj.mainTitle  }}</p>
            </div>
            
            <form class="form" @submit.prevent='add'>
                <div class="question-title">
                    <p>{{ obj.title }}</p>
                </div>
                <div class="question-discription">
                    <p>{{ obj.text }}</p>
                </div>

                <div class="line"></div>

                <div class="answer-wraper">
                    <p class="title-blue">{{ obj.userMainText }}</p>
                    <textarea v-if="!confirm" class='form-text' type="text" v-model='description' :placeholder="obj.placeholder"></textarea>
                    <div v-if="confirm" class='form-text'>
                        <div class="description">
                            {{ description }}
                        </div>
                    </div>
                </div>

                <div v-if="!confirm" class="button-group">
                    <p class="cancel" @click="obj.cancelFunc">キャンセル</p>
                    <button @click="descriptionCheck" class="btn-tr-black-base-sq" 
                    :disabled="alert">{{ obj.buttonText }}</button>
                </div>
                <div v-if="confirm" class="confirm">
                    <p>以上の内容で{{ obj.placeholder }}しますか。</p>
                    <div class="button-group-confirm">
                    <div class="cancel" @click="cancelConfirm">戻る</div>
                    <button class="btn-tr-black-base-sq" 
                    :disabled="alert">{{ obj.buttonText }}</button>
                </div>
                </div>
            </form>
            <div v-if="alert" :class="{'notification-red':alert}">
                <div class="notification-text">
                    文章を入力してください。
                </div>
            </div>
        </div>
    </div>
  
</template>

<script>
// 
export default {
    props:[
        'obj' // includes mainTitle, title, text, userMainText, placeholder, buttonText, cancelFunc, buttonFunc  
    ],
    data() {
        return {
            confirm: false,
            alert: false,
            description:''
        }
    },
    mounted() {
        this.top = window.scrollY
        document.body.style.top = `-${window.scrollY}px`;
        document.body.style.position = 'fixed'
    },
    beforeUnmount() {
        document.body.style.position = ''
        window.scrollTo(0, this.top)
    },
    methods:{
        confirmFunc() {
            this.confirm = true
            this.descriptionCheck()
        },
        cancelConfirm() {
            this.confirm = false
        },
        resetNotifications(){
            this.alert = false
        },
        descriptionCheck(){
             if(this.description==''){
                 this.alert = true
                 setTimeout(this.resetNotifications, 3000)
             } else {
                this.confirm = true
             }
        },
        async add(){
            if(this.alert==false){
                console.log("clicked")
                this.obj.buttonFunc(this.description)
                this.obj.cancelFunc()
            }
         },
    },
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.l-container{
    animation: l-container 3s;
    display: flex;
    flex-direction: column;
    align-items: center;
    position:relative;
    .title-blue{
        margin: 2rem;
    }
    .form{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        .question-discription{
            width:90%;
            min-height: 50px;
            background: rgb(228, 228, 228);
            margin-top: 1rem;
            padding: 0.5rem;
            text-align: left;
            white-space: pre-wrap;
            overflow-y: scroll;

        }
        .line{
            width: 80%;
            border-bottom: 0.2rem solid $dark-blue;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
        .answer-wraper{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            .title-blue{
                margin: 0;
            }
            .form-text{
                background: $back-white;
                padding: 1rem;
                width: 80%;
                height:10rem;
                border: 0.1rem solid $base-color;
                border-radius: 1vh;
                resize: none;
                transition: .5s;
                overflow: scroll;
            }
            .form-text:focus{
                outline: none;
                border: solid $middle-blue;
            }
        }
        .image{
            width:80%;
            display:flex;
            margin:1rem;
        }
        .button-group{
            width: 80%;
            display:flex;
            margin:1rem;
            justify-content: flex-end;
            .cancel{
                border: solid $lite-gray;
                padding: 0.5rem;
                transition: 0.5s;
                min-width: 80px;
            }
            .cancel:hover{
                background: rgb(196, 195, 195);
            }
            .btn-tr-black-base-sq{
                margin-left: 0.8rem;
                padding-right: 0.7rem;
                padding-left: 0.7rem;
                transition: 0.5s;
            }
            .btn-tr-black-base-sq:hover{
                background: $base-color;
                color: white;
                font-weight: bold;
            }
        }
    }
}
.confirm {
    margin-top: 1rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    p{
        font-weight: bold;
        color: $dull-red;
    }
    .button-group-confirm{
        display: flex;
        justify-content: center;
        margin: 1rem 0;
        .cancel{
            border: solid $lite-gray;
            padding: 0.5rem;
            transition: 0.5s;
            min-width: 80px;
            color: black;
        }
        .cancel:hover{
            background: rgb(196, 195, 195);
        }
        .btn-tr-black-base-sq{
                margin-left: 0.8rem;
                padding-right: 0.7rem;
                padding-left: 0.7rem;
                transition: 0.5s;
            }
            .btn-tr-black-base-sq:hover{
                background: $base-color;
                color: white;
                font-weight: bold;
            }
    }
}
.description{
    white-space: pre-wrap;
}
</style>