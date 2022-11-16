const ArtifactConfirmModal = {
    props: ['loadingDelete'],
    template: `
    <div class="modal-component">
        <div class="modal-card">
            <p class="font-bold font-h3 mb-4">Delete bucket?</p>
            <p class="font-h4 mb-4">Are you sure to delete bucket?</p>
            <div class="d-flex justify-content-end mt-4">
                <button type="button" class="btn btn-secondary mr-2" @click="$emit('close-confirm')">Cencel</button>
                <button
                    class="btn btn-basic mr-2 d-flex align-items-center"
                    @click="$emit('delete-bucket')"
                >Delete<i v-if="loadingDelete" class="preview-loader__white ml-2"></i></button>
            </div>
        </div>
    </div>
`
}