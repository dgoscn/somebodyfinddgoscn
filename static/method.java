public void recordCustomEvent(String metricName, Map<String, ?> params) {
    if (StringUtils.isBlank(metricName)) {
        return;
    }

    Span parent = Span.current();
    if (!parent.isRecording()) {
        return; // evita criar spans inúteis
    }

    try {
        metricName = OtelUtil.normalizeMetricName(metricName);
        Attributes attributes = OtelUtil.convertToAttributes(params);

        parent.addEvent(metricName, attributes);

    } catch (Exception ex) {
        LOGGER.warn("Error recording custom event {} with params {}", metricName, params, ex);
    }
}
