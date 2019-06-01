﻿using System.Threading.Tasks;
using ElectionResults.Core.Models;

namespace ElectionResults.Core.Services
{
    public interface IBlobUploader
    {
        Task UploadFromUrl(ElectionResultsFile file);
    }
}