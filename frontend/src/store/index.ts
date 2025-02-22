import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import router from '@/router';
import api from '@/services/api';
import { ProfileModel } from '@/models/profile.model';
import { ServerModel } from '@/models/server.model';
import { AxiosError } from 'axios';


export default createStore({
    state: {
        persistant: {
            token: '',
            wanted_redirect: '',
        },
        global_loading: false,
        selected_server: new ServerModel(),
        profile: new ProfileModel(),
        i18n: ({} as any),
    },
    mutations: {
        set_redirect(state, redirect: string) {
            state.persistant.wanted_redirect = redirect;
        },
        login(state, token: string) {
            state.persistant.token = token;
        },
        logout(state) {
            state.persistant.token = '';
            state.global_loading = false;
        },
        set_profile(state, profile) {
            state.profile.assign(profile);
        },
        set_selected_server(state, server) {
            state.selected_server.assign(server);
        },
        set_global_loading(state, loading) {
            state.global_loading = loading;
        },
        set_i18n(state, i18n) {
            state.i18n = i18n;
        }
    },
    actions: {
        async update_i18n({ commit }) {
            const i18n_response = await api.get_i18n();
            commit('set_i18n', i18n_response.data.i18n);
        },
        async update_profile({ commit }) {
            const profile_response = await api.get_profile();
            commit('set_profile', profile_response.data);
        },
        async update_server({ commit, dispatch, state }) {
            const response = await api.get_guild(state.selected_server.id);
            commit('set_selected_server', response.data);
            await dispatch('update_profile');
        },
        async choose_server({ commit, dispatch }, id: string) {
            commit('set_global_loading', true);
            try {
                const response = await api.get_guild(id);
                commit('set_selected_server', response.data);
                await dispatch('update_profile');
                commit('set_global_loading', false);
            } catch(error: any){
                if (error.response.status == 401) {
                    router.push('login');
                    commit('logout');
                }
            }
        },
    },
    plugins: [createPersistedState({
        paths: ['persistant']
      })]
})
