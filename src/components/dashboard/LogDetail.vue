<template>
    <div class="l-wrapper">
        <div class="main-wrapper">
            <div class='main-quizdetail-wrapper'>
                <div class='l-container'>
                    <div class="close-container">
                        <div @click="close()" class="close">
                            <i class="fas fa-times"></i>
                        </div>
                    </div>
                    <div class="log-index">{{ DetailTagIndex+1 }}</div>
                    <div class="main-detail-container" :class="{'noShow':noShow(logindex)}" v-for="(value, key ,logindex) in loggers.results[DetailTagIndex]"
                        v-bind:key="logindex">
                        <div v-if="logindex!=0&&logindex!=5" class="question-field">
                            <p class="detail-text">{{ key }}</p>
                            <p class="detail-val">{{ value }}</p>
                        </div>
                    </div>
                    <div class="angle-container">                        
                        <i @click="e => DetailTagIndex!=0&& back()" :class="DetailTagIndex==0 ? 'space-left':'fas fa-angle-double-left'"></i>
                        <i @click="e => !nextUrl&&DetailTagIndex!=loggers.results.length-1&& next(e)||typeof nextUrl=='string' && next()" :class="!nextUrl&&DetailTagIndex==loggers.results.length-1 ? 'space-right':'fas fa-angle-double-right'"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// this is common componest to show detail.
// copy logger and make a new vue file to be pasted.
// change the values and url for api request and patch
import axios from 'axios';
export default {
    props:[
        'loggers',
        'currentTagIndex',
        'nextUrl',
        'noMoreUrl',
        'urlForPatch',
    ],
    data(){
        return{
            errorMessage:"components/dashboard/LoggerDetail",
            DetailTagIndex: this.currentTagIndex,
            logIdList: [],
            nextURL: this.nextUrl,
            values: this.loggers
        }
    },
    mounted() {
        this.ckeckedTrue()
        this.top = window.scrollY
        document.body.style.top = `-${window.scrollY}px`;
        document.body.style.position = 'fixed'
    },
    beforeUnmount() {
        document.body.style.position = ''
        window.scrollTo(0, this.top)
         this.patchLogger()
    },
    computed:{
        myQuiz(){
            return this.$store.state.signup.djangoUser.my_quiz[0]
        },
    },
    methods:{
        close(){
            this.$emit('logDetailFalse')
        },
        next(e) {
            if(this.DetailTagIndex!=this.loggers.results.length-1){
                this.DetailTagIndex += 1
                this.ckeckedTrue()
            } else if (this.nextUrl&&this.DetailTagIndex==this.loggers.results.length-1){
                this.getNext()
                this.DetailTagIndex += 1                
            }
        },
        ckeckedTrue() {
            if(!this.loggers.results[this.DetailTagIndex].checked) {
                this.loggers.results[this.DetailTagIndex].checked = true
                this.logIdList.push(this.loggers.results[this.DetailTagIndex].id)
            }
        },
        back() {
            this.DetailTagIndex -= 1
            this.ckeckedTrue()
        },
        getNextUrlFromChild(url) {
            this.$emit('getNextUrlFromChild',url)
        },
        getNextLogger() {
            this.$emit('getNextLogger')
        },
        noShow(index) {
            if(index==0||index==5) {
                return true
            } else {
                return false
            }
        },
        async getNext() {
            await axios
                .get(this.nextURL)
                .then(response => {
                    response.data.results.forEach(e => {
                        this.values.results.push(e)
                    })
                    this.nextURL = response.data.next
                    this.getNextUrlFromChild(this.nextURL)
                    this.ckeckedTrue()
                    })
                .catch(e => {
                    let logger = {
                    message: this.errorMessage + 'getLogger',
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                this.$store.commit('setLogger',logger)
                this.$store.commit("checkDjangoError",e.message)
                this.$store.commit('setIsLoading', false)
                router.push({ name: 'ConnectionError' })
                })
        },
        async patchLogger(){
            this.$store.commit('setIsLoading', true)
            if(this.logIdList.length) {
                await axios
                .patch(this.urlForPatch + this.logIdList)
                .catch(e => {
                    let logger = {
                    message: this.errorMessage + 'patchLogger',
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                this.$store.commit('setLogger',logger)
                this.$store.commit("checkDjangoError",e.message)
                this.$store.commit('setIsLoading', false)
                router.push({ name: 'ConnectionError' })
                })
            }
            this.$store.commit('setIsLoading', false)
        },
    },
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.main-quizdetail-wrapper{
    display: flex;
    justify-content: center;
    position: relative;
    width: 100%;
    .l-container{
        position: relative;
        width: 90%;
        .log-index{
            position: absolute;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid $base-color;
            border-radius: 50vh;
            width: 1.5rem;
            height: 1.5rem;
            margin-left: 0.6rem;
            margin-top: 0.3rem;
            font-weight: bold;
            background: $dark-blue;
            color: $lite-gray;
        }
        .main-detail-container{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-top: 1rem;
            margin-bottom: 1rem;
            .question-field{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                border-bottom: 0.2rem solid $lite-gray;
                width: 90%;
                .detail-text{
                    display: flex;
                    font-weight: bold;
                    font-size: 1.2rem;
                    color: rgb(167, 167, 167);
                }
                .detail-val{
                    font-weight: bold;
                    margin-left: 0.5rem;
                    font-size: 0.9rem;
                    width: 90%;
                    max-width: 90%;
                    overflow-wrap: break-word;
                }
            }
        }
        .noShow{
            display: none;
        }
        .angle-container{
            display: flex;
            justify-content: center;
            width: 100%;
            margin-bottom: 1rem;
            .fa-angle-double-left{
                margin-right: 2rem;
                font-size: 1.2rem;
                color: gray;
                transition: .5s;
            }
            .fa-angle-double-left:hover{
                color: $lite-blue;
            }
            .space-left{
                margin-right: 2rem;
                width: 1.2rem;
            }
            .fa-angle-double-right{
                margin-left: 2rem;
                font-size: 1.2rem;
                color: gray;
                transition: .5s;
            }
            .fa-angle-double-right:hover {
                color: $lite-blue;
            }
            .space-right{
                margin-left: 2rem;
                width: 1.2rem;
            }
        }
    }
}

</style>