const ArtifactStorage = {
    props: ['bucketCount', 'minioQuery'],
    data() {
        return {
            storage: {
                list: {
                    system : {
                        name: 'System',
                        color:'#94E5B0',
                        size: 0,
                    },
                    autogenerated: {
                        name: 'Autogenerated',
                        color: '#96C0FF',
                        size: 0,
                    },
                    local: {
                        name: 'Local',
                        color: '#F2B4B4',
                        size: 0,
                    },
                    free: {
                        name: 'Free',
                        color: '#EAEDEF',
                        size: 0,
                    }
                },
                totalSize: 0,
                maxSize: 0,
            },
        }
    },
    mounted() {
        if (this.bucketCount > 0) {
            this.getData();
        }
    },
    methods: {
        getData() {
            this.fetchStorage().then(data => {
                this.generateStorageList(data);
                this.generateStorageLine(data);
            })
        },
        generateStorageList(data) {
            this.storage.maxSize = data.storage_space_quota.readable;
            this.storage.totalSize = data.total_bucket_size.readable;
            this.storage.list.system.size = data.system_bucket_size.readable;
            this.storage.list.autogenerated.size = data.autogenerated_bucket_size.readable;
            this.storage.list.local.size = data.local_bucket_size.readable;
            this.storage.list.free.size = data.free_space.readable;
        },
        generateStorageLine(data) {
            const systemSize = data.system_bucket_size.bytes / data.storage_space_quota.bytes * 100;
            const autogeneratedSize = data.autogenerated_bucket_size.bytes / data.storage_space_quota.bytes * 100;
            const localSize = data.local_bucket_size.bytes / data.storage_space_quota.bytes * 100;
            const gradientLine = `linear-gradient(to right, ${this.storage.list.system.color} ${systemSize}%,
                ${this.storage.list.autogenerated.color} ${systemSize}% ${autogeneratedSize + systemSize}%,
                ${this.storage.list.local.color} ${autogeneratedSize + systemSize}% ${localSize + autogeneratedSize + systemSize}%,
                ${this.storage.list.free.color} ${localSize + autogeneratedSize + systemSize}%`;
            $('#storageLine').css('background', gradientLine);
        },
        async fetchStorage() {
            const api_url = this.$root.build_api_url('artifacts', 'storage')
            const res = await fetch(`${api_url}/${getSelectedProjectId()}${this.minioQuery}`, {
                method: 'GET',
            })
            return res.json()
        },
    },
    template: `
    <div>
        <div class="d-flex justify-content-between align-items-center pl-3 pr-1 pt-2 pb-1 storage-container" style="border-top: solid 1px #EAEDEF">
            <p class="font-h5 font-semibold text-gray-700 font-h6">Storage use</p>
            <div class="dropdown_info dropup">
                <button class="btn btn-select dropdown-toggle font-weight-400 font-h6" type="button"
                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    {{ storage.totalSize }} / {{ storage.maxSize }}
                </button>
                <ul class="dropdown-menu dropdown-menu-right">
                    <li v-for="storageItem in storage.list" class="dropdown-menu_item dropdown-item d-flex align-items-center">
                        <p class="list-circle mr-2 pb-0 mb-0" :style="{'--bg-color': storageItem.color }">1</p>
                        <p class="w-100 pb-0 mb-0 font-h6 font-weight-400">{{ storageItem.name }}</p>
                        <p class="pb-0 mb-0 ml-4 font-h6 font-weight-400 text-gray-700">{{ storageItem.size }}</p>
                    </li>
                </ul>
            </div>
        </div>
        <div class="px-3 pb-4">
            <div id="storageLine" style="height: 8px; border-radius: 4px; display: inline-block; width: 100%"></div>
        </div>
    </div>
    `
}

register_component('artifact-storage', ArtifactStorage);
