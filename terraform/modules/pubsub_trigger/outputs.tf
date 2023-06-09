output "service_url" {
    value = "https://${google_cloud_run_service.run_service.status[0].url}"
}

output "pubsub_id" {
    value = module.pubsub.id
}