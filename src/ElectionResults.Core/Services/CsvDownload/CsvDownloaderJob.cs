﻿using System.Threading.Tasks;
using ElectionResults.Core.Infrastructure;
using ElectionResults.Core.Models;
using ElectionResults.Core.Services.BlobContainer;

namespace ElectionResults.Core.Services.CsvDownload
{
    public class CsvDownloaderJob: ICsvDownloaderJob
    {
        private readonly IBlobUploader _blobUploader;
        private readonly IElectionConfigurationSource _electionConfigurationSource;

        public CsvDownloaderJob(IBlobUploader blobUploader, IElectionConfigurationSource electionConfigurationSource)
        {
            _blobUploader = blobUploader;
            _electionConfigurationSource = electionConfigurationSource;
        }

        public async Task DownloadFilesToBlobStorage()
        {
            var files = await _electionConfigurationSource.GetListOfFilesWithElectionResults();
            var timestamp = SystemTime.Now.ToUnixTimeSeconds();
            foreach (var file in files)
            {
                file.Name = $"{file.Id}_{timestamp}.csv";
                await _blobUploader.UploadFromUrl(file);
            }
        }
    }
}
