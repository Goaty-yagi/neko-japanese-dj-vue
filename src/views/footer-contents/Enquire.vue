<template>
  <div class="enquire-wrapper">
    <div class="main-wrapper">
      <div class="content-wrapper">
        <div class="title-white">
          <p>問い合わせ</p>
        </div>
        <form action="">
          <div class="enquire-container">
            <div class="enquire-title">名前</div>
            <input
              class="enquire-input"
              type="text"
              v-model="form['名前']"
              placeholder="名前を入力してください"
            />
          </div>
          <div class="enquire-container">
            <div class="enquire-title">メールアドレス</div>
            <input
              class="enquire-input"
              type="text"
              v-model="form['メールアドレス']"
              placeholder="メールアドレスを入力してください"
            />
          </div>
          <div class="enquire-container">
            <div class="enquire-title">問い合わせタイプ</div>
            <div
              class="enquire-type"
              @click="getSelectedItem"
            >
             <FormSelect
            :choicesArray='enquireType'
            :clickTypeConfig='clickTypeConfig'
            optionAlign='left'
            ref='select'
            @getSelectedItem='getSelectedItem'
            />
            </div>
          </div>
          <div class="enquire-container">
            <div class="enquire-title">問い合わせ内容</div>
            <textarea
              class="enquire-text"
              type="text"
              v-model="formTextObj['問い合わせ内容']"
              placeholder="20字以上1000字以内で記入してください"
            >
            </textarea>
          </div>
          <div class="text-length">
            {{ formTextObj["問い合わせ内容"].length }}文字
          </div>
          <div class="faq-comment">
            問い合わせる前に<span @click="goFaq">FAQ</span
            >からよくある質問を確認しましょう。
          </div>
          <div @click="submit()" class="btn-basegra-white-db-sq">送信する</div>
          <div class="error-container">
            <div v-if="showError" :class="{ 'notification-red': showError }">
              <i class="fas fa-exclamation-triangle"></i>
              <div
                v-for="(error, errorindex) in errorArray"
                v-bind:key="errorindex"
              >
                <p>{{ error }}</p>
              </div>
            </div>
          </div>
        </form>
        <AbstractModal
          v-if="confirm"
          :mainText="mainText"
          :formObj="form"
          :formTextareaObj="formTextObj"
          :buttontext="formText"
          :afterClickObj="afterClickObj"
          @buttonFun="confirmedCreate"
          @cancelFun="chancelCreate"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { router } from "/src/main.js";
import AbstractModal from "@/components/parts/AbstractModal.vue";
import FormSelect from "@/components/parts/FormSelect.vue";
import Animation from "@/components/parts/Animation.vue";

export default {
  components: {
    AbstractModal,
    FormSelect,
    Animation
  },
  data() {
    return {
      selectedItem:'',
      clickTypeConfig:{
        function: this.getSelectedItem
       },
      alert: false,
      confirm: false,
      showType: false,
      spin:false,
      mainText: "以下の内容で問い合わせしますか。",
      formText: "問い合わせる",
      afterClickObj: {
        type: "modal",
        title: "問い合わせありがとうございました。",
        text: "内容によっては返信がない場合があります。",
        buttonText: "ホームに戻る",
        buttonFunc: this.goHome,
      },
      enquireType: [
        "利用規約",
        "個人情報の取り扱い",
        "クイズ",
        "コミュニティ",
        "要望",
        "仕事のお問い合わせ",
        "その他",
      ],
      form: {
        名前: "",
        メールアドレス: "",
        問い合わせタイプ: "",
      },
      formTextObj: {
        問い合わせ内容: "",
      },
      showError: false,
      errorArray: [],
      formError: {
        occurred: false,
        名前: "名前を入力してください。",
        longName: "名前は20字以内にしてください。",
        メールアドレス: "メールアドレスを入力してください。",
        wrongMail: "正しいアドレスを入力してください。",
        問い合わせタイプ: "問い合わせタイプを入力してください。",
        text: "問い合わせ内容を入力してください。",
        shortText: "20字以上入力してください。",
        longText: "1000字以内にしてください。",
      },
      copyNode:'',
      animationOut: true,
      functionEnabled: false
    };
  },
  beforeMount() {
        this.$store.commit('setIsLoading', false)
    },
  beforeUnmount() {
    this.$store.commit("showModalFalse");
    this.resetData();
  },
  methods: {
    async createEnquire() {
      try {
        await axios({
          method: "post",
          url: "/api/enquire/",
          data: {
            user_name: this.form["名前"],
            email: this.form["メールアドレス"],
            enquire_type: this.form["問い合わせタイプ"],
            enquire_content: this.formTextObj["問い合わせ内容"],
          },
        });
      } catch (e) {
        let logger = {
          message: this.errorMessage + " enquire" + "couldn't create enquire",
          path: window.location.pathname,
          actualErrorName: e.name,
          actualErrorMessage: e.message,
        };
        this.$store.commit("setLogger", logger);
        this.$store.commit("setIsLoading", false);
        router.push({ name: "ConnectionError" });
      }
    },
    getSelectType(val) {
      this.form["問い合わせタイプ"] = val;
    },
    submit() {
      console.log("scroll",window.scrollY)
      this.errorArray = [];
      this.formError.occurred = false;
      if (this.formTextObj["問い合わせ内容"].length < 20) {
        this.errorArray.push(this.formError["shortText"]);
        this.formError.occurred = true;
      } else if (this.formTextObj["問い合わせ内容"].length >= 1000) {
        this.errorArray.push(this.formError["LongText"]);
        this.formError.occurred = true;
      }
      for (let i of Object.keys(this.form)) {
        if (!this.form[i]) {
          this.errorArray.push(this.formError[i]);
          this.formError.occurred = true;
        } else if (i == "メールアドレス") {
          if (!this.validEmail(this.form[i])) {
            this.errorArray.push(this.formError["wrongMail"]);
            this.formError.occurred = true;
          }
        } else if (i == "名前") {
          if (this.form[i].length > 20) {
            this.errorArray.push(this.formError["longName"]);
            this.formError.occurred = true;
          }
        }
      }
      if (!this.formError.occurred) {
        this.confirm = true;
        this.$store.commit("showModalTrue");
      } else {
        this.showError = true;
        this.setTime(this.showErrorFalse);
      }
    },
    validEmail: function (email) {
      var re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    showErrorFalse() {
      this.showError = false;
    },
    confirmedCreate() {
      this.createEnquire();
    },
    chancelCreate() {
      this.confirm = false;
      console.log("cancel", this.confirm);
    },
    setTime(callback) {
      setTimeout(callback, 3000);
    },
    goHome() {
      router.push("/");
    },
    resetData() {
      this.form["名前"] = "";
      this.form["メールアドレス"] = "";
      this.form["問い合わせタイプ"] = "";
      this.form["問い合わせ内容"] = "";
      this.showType = false;
      this.showError = false;
      this.formError.occurred = false;
    },
    goFaq() {
      const url = window.location.origin + "/faq";
      window.open(url);
      // router.push({name:'Faq'})
    },
    getSelectedItem() {
      this.form["問い合わせタイプ"] = this.$refs.select.chosenItem
      console.log(this.form["問い合わせタイプ"])
    }
  },
};
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";

.enquire-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}
.content-wrapper {
  .title-white {
    margin-bottom: 2rem;
  }
  .enquire-container {
    position: relative;
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 1rem;
    .enquire-title {
      position: absolute;
      left: 0;
      top: 0;
      margin-left: 5%;
      height: 20px;
      color: white;
      font-weight: bold;
      border-bottom: solid $dark-blue;
    }
    .enquire-input {
      width: 90%;
      margin-top: 25px;
      height: 40px;
      padding: 0.3rem;
      border-radius: 8px;
      font-size: 1.2rem;
      transition: 0.2s;
    }
    .enquire-input:focus {
      border: solid $base-color;
    }
    .enquire-text {
      width: 90%;
      margin-top: 25px;
      height: 300px;
      padding: 1rem;
      // margin-bottom: 1rem;
      resize: none;
      font-size: 1.2rem;
      border-radius: 8px;
      border-top: solid black;
      border-left: solid black;
      border-right: solid gray;
      border-bottom: solid gray;
      transition: 0.2s;
    }
    .enquire-text:focus {
      outline: none;
      border: solid $base-color;
    }
    .enquire-type:hover {
      border: solid $base-color;
    }
    .enquire-type {
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
      width: 90%;
      margin-top: 25px;
      height: 40px;
      padding: 0.3rem;
      font-size: 1.2rem;
      transition: 0.2s;
      background: white;
      border-radius: 8px;
      border-top: solid black;
      border-left: solid black;
      border-right: solid gray;
      border-bottom: solid gray;
      .type-select {
        position: absolute;
        width: 100%;
        min-height: 80px;
        // top: 100px;
        // opacity: 0;
        background: rgba(37, 38, 62, 0.95);
        border-radius: 8px;
        border: solid $dark-blue;
        color: white;
        overflow: hidden;
        animation: bottomToUp 0.5s ease-out forwards;
        z-index: 1;
      }
      .select-undisplay{
        display: none;
      }
      .selectOut {
        animation: bottomToUp 0.5s ease-out reverse forwards;
      }
      .selectClose {
        position: absolute;
        width: 100%;
        min-height: 80px;
        // top: 100px;
        // opacity: 0;
        background: rgba(37, 38, 62, 0.95);
        border-radius: 8px;
        border: solid $dark-blue;
        color: white;
        overflow: hidden;
        animation: bottomToUp 0.5s ease-out reverse forwards;
        z-index: 1;
      }
    }
    .fa-angle-down {
      transition: 0.5s;
    }
    .lotate {
      transform: rotate(180deg);
    }
  }
  .btn-basegra-white-db-sq {
    padding: 0.1rem 0.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  .error-container {
    position: absolute;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    left: 0;
    .notification-red {
      .fa-exclamation-triangle {
        color: red;
      }
      div {
        color: red;
        margin-top: 0.5rem;
        font-weight: bold;
      }
    }
    .l-wrapper {
      z-index: 1;
    }
    .l-container {
      padding: 1rem;
      font-weight: bold;
      .created-header {
        color: $dull-red;
        margin-bottom: 1rem;
      }
    }
    .button-container div {
      margin-top: 1.5rem;
      padding: 0 1rem;
      border: solid gray;
      display: inline-block;
      transition: 0.5s;
    }
    .button-container div:hover {
      border: solid $dark-blue;
      color: gray;
    }
  }
}
.confirm {
  padding: 1rem;
  .confiem-header {
    font-size: 1.3rem;
    margin: 0.5rem 0;
    color: $dull-red;
  }
  p {
    margin-bottom: 1rem;
    font-weight: bold;
    font-size: 0.9rem;
  }
  .each-container {
    width: 100%;
    display: flex;
    justify-content: center;
    .each-title {
      flex-basis: 45%;
      width: 50%;
      display: flex;
      justify-content: flex-end;
    }
    .space {
      flex-basis: 5%;
    }
    .content {
      flex-basis: 45%;
      width: 45%;
      display: flex;
    }
  }
  .button-container {
    width: 100%;
    display: flex;
    justify-content: center;
    div {
      margin: 0 0.5rem;
      border: solid gray;
      padding: 0.2rem 0.5rem;
      transition: 0.5s;
      font-weight: bold;
    }
    div:hover {
      color: gray;
    }
  }
  .text-container {
    width: 100%;
    display: flex;
    flex-direction: column;
  }
}
.text-length {
  color: white;
  text-align: right;
  margin-right: 0.5rem;
}
.fa-edit {
  position: absolute;
  right: 1rem;
  transition: 0.3s;
}
.fa-edit:hover {
  color: gray;
}
.faq-comment {
  color: whitesmoke;
  margin-bottom: 1rem;
  font-weight: bold;
  text-decoration: underline;
  
  span:hover {
    color: $base-color;
    cursor: pointer;
  }
}
.type {
  padding: 0.5rem 0;
  transition: 0.5s;
}
.type:hover {
  display: block;
  background: rgba(59, 60, 96, 0.75);
}
.form-select-parent {
  position: relative;
    display: flex;
    justify-content: center;
    width: 90%;
    margin-top: 1rem;
    background: white;
    padding: 1rem;
}
@keyframes bottomToUp {
  0% {
    opacity: 0;
    top: 100px;
  }
  100% {
    opacity: 1;
    top: 45px;
  }
}
</style>