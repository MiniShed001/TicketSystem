import {
	createSSRApp
} from "vue";
import App from "./App.vue";
import userStore from "./store/user.js";

export function createApp() {
	const app = createSSRApp(App);
	// 挂载全局用户状态
	app.config.globalProperties.$user = userStore;
	return {
		app,
	};
}
