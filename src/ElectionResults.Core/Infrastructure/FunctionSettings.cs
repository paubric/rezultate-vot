﻿using System;
using Microsoft.Extensions.Configuration;

namespace ElectionResults.Core.Infrastructure
{
    public static class FunctionSettings
    {
        private static IConfigurationRoot _config;

        public static void Initialize(Microsoft.Azure.WebJobs.ExecutionContext context)
        {
            var configurationBuilder = new ConfigurationBuilder();
            _config = configurationBuilder
                .SetBasePath(context.FunctionAppDirectory)
                .AddJsonFile("local.settings.json", optional: true, reloadOnChange: true)
                .AddEnvironmentVariables()
                .AddJsonFile("secrets.settings.json", optional: true, reloadOnChange: true)
                .Build();
            Console.WriteLine(_config["AzureWebJobsStorage"]);
        }

        public static string AzureStorageConnectionString => _config["AzureWebJobsStorage"];

        public static string BlobContainerName => _config["BlobContainerName"];

        public static string AzureTableName => _config["AzureTableName"];
    }
}
