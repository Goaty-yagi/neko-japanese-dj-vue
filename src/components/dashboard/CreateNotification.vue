<template>
    <div class="create-notification-wrapper" :class="{'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
            <div class="create-notification-container" v-if="$store.state.isLoading==false">
                <form @submit.prevent='submit' class="field-wrapper">
                    <div class="enquire-container">
                        <div class="enquire-title">Title</div>
                        <input class="enquire-input" type="text" maxlength='20' v-model='form["タイトル"]' placeholder="タイトルを入力してください">
                    </div>
                    <div class="enquire-container">
                        <div class="enquire-title">お知らせタイプ</div>
                        <div class="enquire-type"
                        >
                         <FormSelect
                        :choicesArray='noteType'
                        optionAlign='left'
                        :clickTypeConfig='clickTypeConfig'
                        ref='select'
            />
                        </div>
                    </div>
                    <div class="enquire-container">
                        <div class="enquire-title">投稿時間</div>
                        <input class="enquire-input" type="datetime-local" v-model='form["投稿時間"]' >
                    </div>
                    <div class="enquire-container">
                        <div class="enquire-title">内容</div>
                        <textarea class="enquire-text" type="text" v-model='formTextObj["内容"]' placeholder="20字以上1000字以内で記入してください"></textarea>
                    </div>
                    <div class="image-button-container">
                        <div class="image-bottun" @click='handleShowThumbnail'>
                            <p v-if="!image">画像を入れますか？</p>
                            <p v-if="image">画像を変更しますか？</p>
                        </div>
                        <div v-if="image" class="image-container">
                            <img class="image" :src="image">
                        </div>
                        <div class="error-container">
                            <div v-if='showError' :class="{'notification-red':showError}">
                                <i class="fas fa-exclamation-triangle"></i>
                                <div v-for="(error,errorindex) in errorArray" 
                                    v-bind:key="errorindex">
                                    <p>{{ error }}</p>
                            </div>
                        </div>
                        </div>
                    </div>
                    <div class="button-container">
                        <button class='fbottun' ref='bform' id=''>作成する</button>
                    </div>
                </form>
            </div>
        </div>
        <Thumbnail v-if="showThumbnail"
        :ratio="1.78"
        @showThumbnailFalse="showThumbnailFalse"
        @setImageBlob="setImageBlob"
        />
        <AbstractModal
        v-if='confirm'
        :mainText='confirmInfo.text'
        :noteText='confirmInfo.noteText'
        :formObj='form'
        :formTextareaObj='formTextObj'
        :buttontext='confirmInfo.buttonText'
        :image='image'
        :afterClickObj="afterClickObj"
        @buttonFun='createNotification'
        @cancelFun='handelConfirm'
        />
    </div>
</template>

<script>
import axios from 'axios'
import Thumbnail from '@/components/account/Thumbnail.vue'
import AbstractModal from '@/components/parts/AbstractModal.vue'
import FormSelect from "@/components/parts/FormSelect.vue";
// import QuizConfirm from '@/components/dashboard/QuizConfirm.vue'
const initialState = () => {
  return {
    showThumbnail: false,
            image:'',
            showType: false,
            confirm: false,
            showError :false,
            confirmInfo: {
                text:'以下の内容で作成しますか。',
                noteText:'',
                buttonText:"作成"
            },
            noteType: [
                'アップデート',
                'お知らせ',
                '重要',
                'その他'
            ],
            form: {
                タイトル:'',
                お知らせタイプ:'',
                投稿時間:''
            },
            formTextObj:{
                "内容":''
            },
    //         afterClickObj: {
    //             type: "toast",
    //             // title: "問い合わせありがとうございました。",
    //             text: "作成しました。",
    //             // buttonText: "ホームに戻る",
    //             // buttonFunc: this.goHome,
    //   },
            // afterClickObj:{
            //     type:'toast',
            //     // title:'問い合わせありがとうございました。',
            //     text:'作成しました。',
            //     errorText:'作成できませんでした。しばらく経ってからもう一度お試しください。',
            //     // buttonText:'ホームに戻る',
            //     // buttonFunc:this.goHome,
            //     afterCreatedFunc: this.confirmedCreate // for toast
            // },
            formError:{
                occurred:false,
                名前:'名前を入力してください。',
                longName:'タイトルは20字以内にしてください。',
                text:'問い合わせ内容を入力してください。',
                shortText:'20字以上入力してください。',
                longText:'1000字以内にしてください。'
            },
            errorArray:[]
  }
}
export default {
    components: {
        Thumbnail,
        AbstractModal,
        FormSelect
        // QuizConfirm,
    },
    data: () => { 
        return initialState()
    },
    computed: {
        afterClickObj() {
            return {
                type:'toast',
                text:'作成しました。',
                errorText:'作成できませんでした。しばらく経ってからもう一度お試しください。',
                afterCreatedFunc: this.confirmedCreate // for toast
            }
        },
        clickTypeConfig(){
            return {
                function: this.getSelectType

            }
        },
    },
    methods:{
        resetWindow: function (){
            Object.assign(this.$data, initialState());
        },
        submit() {
            this.checkError()
        },
        handelConfirm() {
            this.confirm = !this.confirm
        },
        async createNotification() {
            console.log("IN_CREATE")
            const data = {
                'title': this.form['タイトル'],
                'type': this.form['お知らせタイプ'],
                'body': this.formTextObj['内容'],
                'issued_date':  new Date(this.form["投稿時間"])
            }
            console.log("DATA", data)
            const response = await axios({
                method: 'post',
                url: '/api/notification/create',                            
                data: data,
            }).catch((e) => {
                console.log("ERROR", e)
            })
            if(this.image) {
                const formdata = new FormData
                formdata.append('image',this.blob,`${this.blob}.png`)
                axios
                .patch(
                    `/api/notification/detail/${response.data.slug}`,formdata)
            }
            this.clearForm()
        },
        checkError() {
            this.errorArray = []
            this.formError.occurred = false
            console.log("got2", this.form)
            for(let i of Object.keys(this.form)) {
                if(!this.form[i]) {
                    console.log("i",i, this.form[i], 'yoi',this.form["お知らせタイプ"])
                    this.errorArray.push(i + 'を入力してください。')
                    this.formError.occurred = true
                }
                else if(i == 'タイトル') {
                    if(this.form[i].length > 20) {
                        this.errorArray.push(this.formError["longName"])
                        this.formError.occurred = true
                    }
                }

            }
            if(this.formTextObj['内容'].length < 20) {
                this.errorArray.push(this.formError["shortText"])
                this.formError.occurred = true
            } 
            else if(this.formTextObj['内容'].length >= 1000) {
                this.errorArray.push(this.formError["LongText"])
                this.formError.occurred = true

            }
            if(!this.formError.occurred){
                this.timeCheck()
                this.confirm = true
                this.$store.commit('showModalTrue')
            } else {
                this.showError = true
                this.setTime(this.showErrorFalse)
            }
        },
        setTime(callback){
            setTimeout(callback,3000)
        },
        showErrorFalse(){
            this.showError = false
        },
        confirmedCreate(){
            this.confirm = false
        },
        
        handleShowThumbnail(){
            this.showThumbnail = true
        },
        showThumbnailFalse(){
            this.showThumbnail = false
        },
        setImageBlob(blob,url) {
            this.image = url
            this.blob = blob
        },
        showTypeHandle() {
            this.showType = !this.showType
        },
        getSelectType(){
            this.form["お知らせタイプ"] = this.$refs.select.chosenItem
        },
        clearForm(){
            this.form['タイトル'] = '',
            this.form['お知らせタイプ'] = '',
            this.form['投稿時間'] = '',
            this.$refs.select.clearChosenItem()
            this.formTextObj['内容'] = ''
        },
        timeCheck() {
            const localDate = new Date()
            const planedDate = new Date(this.form["投稿時間"])
            // true means future
            this.confirmInfo.noteText = localDate < planedDate?'':'投稿時間が過去になっているため、すぐに表示されます。'
        }
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.create-notification-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 2reml;
}
.enquire-container{
    position: relative;
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 1rem;
    .enquire-title{
        position: absolute;
        left: 0;
        top: 0;
        margin-left: 5%;
        height: 20px;
        color: white;
        font-weight: bold;
        border-bottom: solid $dark-blue;
    }
    .enquire-input{
        width: 90%;
        margin-top: 25px;
        height: 40px;
        padding: 0.3rem;
        font-size: 1.2rem;
        transition: .2s;
    }
    .enquire-input:focus{
        border: solid $base-color;
    }
    .enquire-text{
        width: 90%;
        margin-top: 25px;
        height: 300px;
        padding: 1rem;
        margin-bottom: 1rem;
        resize: none;
        font-size: 1.2rem;
        transition: .2s;

    }
    .enquire-text:focus{
            outline: none;
            border: solid $base-color;
    }
    .enquire-type{
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 90%;
        margin-top: 25px;
        height: 40px;
        padding: 0.3rem;
        font-size: 1.2rem;
        transition: .2s;
        background: white;
        .type-select{
            position: absolute;
            width: 100%;
            min-height: 80px;
            top: 35px;
            background: rgba(252, 252, 252, 0.95);;
            z-index: 1;
            .type{
                padding: 0.5rem 0;
                transition: .5s;
            }
            .type:hover{
                display: block;
                background: $lite-gray;
            }
        }
    }
    .fa-angle-down{
        transition: .5s;
    }
    .lotate{
        transform:rotate(180deg);
    }
}
.image-button-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 2rem;
}
.image-bottun{
    margin-top: 1rem;
    color: $lite-gray;
    border: solid gray;
    padding: 0.1rem 0.7rem;
    transition: .5s;
}
.image-bottun:hover {
    border: solid $base-color;
}
.image-container{
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 1rem;
    .image{
        width: 100%;
    }
}
.button-container {
    margin-bottom: 3rem;
}
.error-container{
    position: absolute;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    left: 0;
    .notification-red{
        .fa-exclamation-triangle{
            color: red;
        }
        div{
            color: red;
            margin-top: 0.5rem;
            font-weight: bold;
        }
    }
}
.fa-edit{
    position: absolute;
    right: 1rem;
    transition: .3s;

}
.fa-edit:hover{
    color: gray;
}
.enquire-input[type="datetime-local"]::-webkit-calendar-picker-indicator {
//   display: none;
    padding-right: 1rem;
    filter: invert(50%);
}
.enquire-input[type="datetime-local"]:focus{
        outline: none;
        border: solid $base-color;
}
</style>