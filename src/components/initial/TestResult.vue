<template>
    <div class='testresult-wrapper'>
        <div class="confetti-container">
            <ConfettiExplosion
            v-if="resultText!=='DOWN'||init"
            :particleCount="particleCount"
            :particleSize="12"
            :duration="3500"
            :force="0.9"
            :stageHeight="1200"
            :stageWidth="1600"
            :shouldDestroyAfterDone="true"/>
        </div>
        <div v-if="showResultNotification" class="progress-container">
            <div class="progress-inner-container">
                <p class="result-text"> {{ resultText }}</p>
            </div>
            <p class="progress-text"> {{ gradeForConvert }} Lv, {{ startGradeAndLevel.level }} => 
            {{ finalResult.grade }} Lv, {{ finalResult.level }}
            </p>
            <router-link class="home-link" :to="{name:'Home'}"><i class="fas fa-home"></i>Return to Home</router-link>
        </div>
        <h1 class='is-size-1 has-text-white'>-結果-</h1>
        <p class='result-text'>あなたのレベルは…</p>
        <div class="diamond-wrapper">
            <div class='dwrapper1'>
                <div class='diamond-outer'/>
            </div>
            <div class='dwrapper2'>
                <div class='diamond'/>
            </div>
            <div class='text-wrapper'>
                <p class='text'>{{ finalResult.grade }}</p>
                <p class='level-text'>Lv,{{ finalResult.level }}</p>
            </div>
        </div>
        <div class='font-wrapper'>
            <i class="fab fa-angellist"></i>
        </div>
        <transition name="notice">
            <Notification
            v-if="showNotification"/>
        </transition>
    </div>
</template>

<script>
import Notification from '@/components/initial/Notification.vue';
import ConfettiExplosion from "vue-confetti-explosion";
export default {
    props:[
        "finalResult",
        "init",
        "startGradeAndLevel"
    ],
     components: {
        Notification,
        ConfettiExplosion
  },
  data(){
        return{
            particleCount:160,
            showNotification: false,
            showResultNotification: false,
            resultText: '',
            gradeDict:{
                '超初級':0,
                '初級':10,
                '中級':20,
                '上級':30
            },
            resultTextObjects:{
                'up':'UP',
                'stay':'STAY',
                'down':'DOWN'
            },
        }
    },
    computed:{
        gradeForConvert(){
            return this.$store.getters.gradeForConvert
        }

    },
    mounted(){
        this.showConfetti()
        console.log("MOUNT", this.init)
        if(this.init){
            setTimeout(() =>{
                this.handleShowNotification()
            },3000
            )
        } else {
            setTimeout(() =>{
                this.handleShowResultNotification()
            },2000
            )
        }
    },
    methods:{
        handleShowNotification(){
            this.showNotification = !this.showNotification

        },
        showConfetti(){
            if(this.gradeDict[this.finalResult.grade] > this.gradeDict[this.gradeForConvert]){
                this.$store.commit('convertGradeFromIntToID',this.startGradeAndLevel.grade)
                this.handleResultText('up')
                return true
            }
            else if(this.gradeDict[this.finalResult.grade] == this.gradeDict[this.gradeForConvert]) {
                if(this.finalResult.level > this.startGradeAndLevel.level){
                    this.handleResultText('up')
                    return true 
                } else if(this.finalResult.level == this.startGradeAndLevel.level){
                    this.handleResultText('stay')
                    this.ConfettiParameterHandler()
                    return false
                }
                else{
                    this.handleResultText('down')
                    return false
                }
            }else{
                this.handleResultText('down')
                return false
            }
        },
        ConfettiParameterHandler() {
            this.particleCount = 40
        },
        handleResultText(status){
            this.resultText = this.resultTextObjects[status]
            // return this.resultText[status]
        },
        handleShowResultNotification() {
            if(!this.init){
                setTimeout(
                this.showResultNotificationTrue(),3000
                )
            }
        },
        showResultNotificationTrue() {
            this.showResultNotification = true
        }
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.testresult-wrapper{
    position: relative;
    .confetti-container{
        position: absolute;
        top: 30%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index:2
    }
    .progress-container{
        position: absolute;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: solid $base-color;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        min-height: 120px;
        width: 100%;
        background: $back-tr-white;
        z-index: 1;
        .progress-inner-container{
            height: 40%;
            width: 100%;
            background: $dark-blue;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .progress-text{
            margin-top: 1rem;
            font-size: 1.5rem;
            font-weight: bold;
            color: $dull-red;
        }
        .home-link {
            margin:1rem 0;
            font-weight: bold;
        }
        .fa-home{
            margin-right: 0.5rem;
        }
        .result-text{
            color: black;
            bottom: 0;
            font-size: 1.5rem;
            font-weight: bold;
            color: $lite-gray;
        }
    }
}
    /* // this is only for i phone5 */
  @media(max-width: 355px){
      
        .result-text{
            font-size:1.5rem;
            color:white;
            }
        .diamond-wrapper{
            position:relative;
            margin-top:-2rem;
            margin-bottom:auto;    
            }
        .diamond-outer{
            border: 7.5rem solid transparent;
            border-bottom: 5.5rem solid orange;
            position: relative;
            top: -5rem;
            width: 0;
            height: 0;
            margin: 0 auto;
        }
        .diamond-outer:after{
            content: '';
            position: absolute;
            left: -7.5rem;
            top: 5.5rem;
            width: 0;
            height: 0;
            border: 7.5rem solid transparent;
            border-top: 5.5rem solid orange;
                }        
        .diamond{
            width: 0;
            height: 0;
            border: 7rem solid transparent;
            border-bottom: 5rem solid white;
            position: relative;
            top: -17rem;
            margin: 0 auto;
                }
        .diamond:after{
            content: '';
            position: absolute;
            left: -7rem;
            top: 5rem;
            width: 0;
            border: 7rem solid transparent;
            border-top: 5rem solid white;
            }
        .text{
            font-size:2rem;
            color:black;
            font-weight: bold;
            }
        .text-wrapper{
            position:absolute;
            left: 0;
            right: 0;
            margin: 0 auto;
            top:6.5rem;
            }
        .font-wrapper{
            font-size:10rem;
            color:orange;
            margin-top:-13rem;
        }
    }
    @media(min-width: 356px){
    .result-text{
            font-size:2rem;
            color:white;
            }
    .diamond-wrapper{
        position:relative;     
        }
    .dwrapper1{
        position:absolute;
        left: 0;
        right: 0;
        margin: 0 auto;
        
    }
    .dwrapper2{
        position:absolute;
        left: 0;
        right: 0;
        margin: 0 auto;
    }
    .diamond-outer {
        width: 0;
        height: 0;
        border: 8.5rem solid transparent;
        border-bottom: 5.5rem solid orange;
        position: relative;
        top: -5rem;
        margin: 0 auto;

    }   
    .diamond-outer:after {
        content: '';
        position: absolute;
        left: -8.5rem; top:5.5rem;
        width: 0;
        height: 0;
        border: 8.5rem solid transparent;
        border-top: 5.5rem solid orange;
    }

    .diamond {
        width: 0;
        height: 0;
        border: 8rem solid transparent;
        border-bottom: 5rem solid white;
        position: relative;
        top: -4rem;
        margin: 0 auto;
    }
    .diamond:after {
        content: '';
        position: absolute;
        left: -8rem; top:5rem;
        width: 0;
        height: 0;
        border: 8rem solid transparent;
        border-top: 5rem solid white;
        
    }
    .text-wrapper{
        position:absolute;
        left: 0;
        right: 0;
        margin: 0 auto;
        top:7.5rem;
    }
    .text{
        font-size:2rem;
        color:black;
        font-weight: bold;
        margin: 0 auto;
    }
    .level-text{
        font-weight: bold;
        font-size: 1.5rem;
    }
    .font-wrapper{
        font-size:10rem;
        color:orange;
        margin-top:15rem;
    }
}
</style>